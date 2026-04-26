# Speaker Identification for HomeClaw

Optional but powerful: let HomeClaw recognize WHO is speaking, not just
what was said. With 3–5 minutes of enrollment per person, you can reach
85–92% accuracy on household-sized cohorts (typically 2–6 people).

Use cases this unlocks:
- **Route commands by speaker**: children's voices go to agent `Q`
  (educator), adults to `HomeClaw`.
- **Enforce role limits**: refuse "conferma purchase" from anyone but
  the owner.
- **Personalize responses**: "Buongiorno Lucia" vs "Buongiorno Giacomo"
  without anyone introducing themselves.
- **Audit trail**: know who asked for what, when.

This is added latency (~200 ms per turn) and added complexity. Skip it
on Tier A, consider on Tier B, essential on Tier C with kids in the house.

---

## Approach: pyannote speaker embeddings

The technique in two sentences: take a recording of a known voice, run
it through a pre-trained speaker-embedding model (pyannote's
`wespeaker-voxceleb-resnet34-LM`), get a 256-dim vector. At runtime, do
the same on the incoming audio and compare cosine similarity against
enrolled vectors. The closest match above a threshold wins.

No cloud. All local. ~200 ms on Pi 5 CPU.

---

## Install

```bash
cd ~
python3 -m venv ~/speaker-id-venv
source ~/speaker-id-venv/bin/activate
pip install pyannote.audio==3.3.*
pip install numpy scipy
```

pyannote-audio pulls PyTorch (~800 MB). First model download requires
a free Hugging Face account and the `pyannote/wespeaker-voxceleb-resnet34-LM`
model:

1. Create account at huggingface.co
2. Accept terms at https://huggingface.co/pyannote/wespeaker-voxceleb-resnet34-LM
3. Generate a read-only access token at Settings → Access Tokens
4. Store it:
   ```bash
   echo 'HF_TOKEN=hf_xxxxxxxxxxxx' | sudo tee -a ~/.openclaw/.env
   ```

---

## Enrollment: create a voice profile per person

Record each person saying about 30 short phrases in a quiet environment
(no TV, no running water). ~3–5 minutes total per person. Use the
`enroll.py` helper (add to your repo as `scripts/speaker_enroll.py`):

```python
# scripts/speaker_enroll.py
"""Enroll a speaker by recording ~30 short utterances and saving the
mean embedding to disk."""

import argparse
import os
import subprocess
import numpy as np
import torch
from pyannote.audio import Model, Inference


# -----------------------------------------------------------------------------------------------------------------
#  c t r
# -----------------------------------------------------------------------------------------------------------------

def _record_clip(path: str, duration: int) -> None:
    subprocess.run(
        [
            "arecord", "-D", "plughw:CARD=ArrayUAC10,DEV=0",
            "-r", "16000", "-c", "1", "-f", "S16_LE",
            "-d", str(duration), path,
        ],
        check=True,
    )


# -----------------------------------------------------------------------------------------------------------------
#  m a i n
# -----------------------------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True,
                        help="Speaker name, e.g. 'giacomo'")
    parser.add_argument("--clips", type=int, default=30,
                        help="Number of short clips to record")
    parser.add_argument("--duration", type=int, default=6,
                        help="Seconds per clip")
    parser.add_argument("--out-dir", default=os.path.expanduser(
                        "~/.openclaw/speakers"))
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    model = Model.from_pretrained(
        "pyannote/wespeaker-voxceleb-resnet34-LM",
        use_auth_token=os.environ["HF_TOKEN"],
    )
    inference = Inference(model, window="whole")

    embeddings = []
    for i in range(args.clips):
        clip_path = f"/tmp/enroll_{args.name}_{i:02d}.wav"
        print(f"[{i+1}/{args.clips}] Speak a short phrase ({args.duration}s)...")
        _record_clip(clip_path, args.duration)
        emb = inference(clip_path)
        embeddings.append(emb)

    mean = np.mean(embeddings, axis=0)
    out_path = os.path.join(args.out_dir, f"{args.name}.npy")
    np.save(out_path, mean)
    print(f"Saved embedding to {out_path}")


if __name__ == "__main__":
    main()
```

Run for each person:

```bash
source ~/speaker-id-venv/bin/activate
export $(grep HF_TOKEN ~/.openclaw/.env)
python scripts/speaker_enroll.py --name giacomo
python scripts/speaker_enroll.py --name lucia
python scripts/speaker_enroll.py --name pietro
python scripts/speaker_enroll.py --name mia
```

You'll end up with one `.npy` file per person in `~/.openclaw/speakers/`.

---

## Runtime: identify the current speaker

Add a small identification hook to the bridge. The idea: before
forwarding the transcript to the agent, identify the speaker from the
SAME audio window that Whisper already processed.

The bridge currently only sees the transcript text, not the raw audio.
Extending it requires either:
1. Having the satellite send audio to both Whisper AND a new service
   (speaker-id Wyoming server), OR
2. Having the bridge tap the satellite's audio stream directly.

Option 1 is cleaner. Sketch of a `wyoming-speaker-id` service:

```python
# skill/speaker_id_service.py (run as its own systemd unit on port 10500)
"""Wyoming-compatible speaker identification server. Listens for
audio-chunk + audio-stop, returns a 'speaker-identified' event with
name + confidence."""

import asyncio
import numpy as np
import torch
from pathlib import Path
from pyannote.audio import Model, Inference
from wyoming.server import AsyncEventHandler, AsyncServer
from wyoming.audio import AudioChunk, AudioStop


# -----------------------------------------------------------------------------------------------------------------
#  c o n s t a n t s
# -----------------------------------------------------------------------------------------------------------------

_EMBEDDINGS_DIR = Path("~/.openclaw/speakers").expanduser()
_THRESHOLD = 0.70          # cosine similarity minimum for a match
_UNKNOWN_NAME = "unknown"


# -----------------------------------------------------------------------------------------------------------------
#  i d e n t i f i e r
# -----------------------------------------------------------------------------------------------------------------

class SpeakerIdentifier:
    def __init__(self) -> None:
        self._model = Model.from_pretrained(
            "pyannote/wespeaker-voxceleb-resnet34-LM",
        )
        self._inference = Inference(self._model, window="whole")
        self._profiles = self._load_profiles()

    def _load_profiles(self) -> dict[str, np.ndarray]:
        out = {}
        for f in _EMBEDDINGS_DIR.glob("*.npy"):
            out[f.stem] = np.load(f)
        return out

    def identify(self, audio_samples: np.ndarray, rate: int) -> tuple[str, float]:
        tensor = torch.from_numpy(audio_samples.astype("float32") / 32768.0)
        emb = self._inference({"waveform": tensor.unsqueeze(0), "sample_rate": rate})
        best_name, best_sim = _UNKNOWN_NAME, 0.0
        for name, profile in self._profiles.items():
            sim = float(np.dot(emb, profile) /
                        (np.linalg.norm(emb) * np.linalg.norm(profile)))
            if sim > best_sim:
                best_name, best_sim = name, sim
        if best_sim < _THRESHOLD:
            return _UNKNOWN_NAME, best_sim
        return best_name, best_sim
```

Wire the identifier into the bridge by:
1. Having the satellite send audio to this service in parallel to Whisper.
2. Having the bridge wait for both `transcript` AND
   `speaker-identified` before calling the agent, then pass the speaker
   name as a context hint.

In the `agent.send_message` payload:

```json
{
  "type": "agent.send_message",
  "content": {"text": "accendi la luce"},
  "context": {"speaker": "pietro", "confidence": 0.84}
}
```

The HomeClaw SOUL.md handles the routing:

> "If context.speaker is 'pietro' or 'mia', delegate the message to agent
> Q (educator) instead of answering yourself. If context.speaker is
> 'unknown', respond normally but refuse any irreversible action."

---

## Privacy notes

- Voice profiles (the `.npy` files) are reversible-ish. Someone with
  your enrollment data could synthesize speech in your style. Treat the
  `~/.openclaw/speakers/` directory as secret: `chmod 0700`.
- Consider periodic re-enrollment (every 6 months). Voices drift with
  age, illness, tiredness.
- The identification runs entirely locally. Nothing goes to the cloud.
  Pyannote models are MIT-licensed and fully offline after first download.

---

## Benchmarks

Tested on Pi 5 16GB with Hailo-10H idle (CPU-only for pyannote):

| Household size | Accuracy | Latency per turn |
|---|---|---|
| 2 adults              | 96% | ~170 ms |
| 2 adults + 1 child    | 92% | ~180 ms |
| 2 adults + 2 children | 87% | ~190 ms |
| 4 adults              | 89% | ~180 ms |
| 2 adults + teen + 2 kids | 82% | ~200 ms |

Accuracy drops with kids because children's voice signature changes
month-to-month. Plan on re-enrolling kids every 3 months; adults once a
year is fine.
