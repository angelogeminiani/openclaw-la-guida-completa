# Training a custom "Ehi Claw" wake word

openWakeWord uses neural networks trained on thousands of synthetic and
real examples of a phrase. You can train one for "Ehi Claw" yourself with
zero GPU of your own, using Google Colab's free tier.

## The quick path (1 hour)

1. Open the automated training notebook:
   https://colab.research.google.com/github/dscripka/openWakeWord/blob/main/notebooks/automatic_model_training_simple.ipynb

2. In the first code cell, set:
   ```python
   target_phrase = "Ehi Claw"
   number_of_examples = 5000       # default is fine
   number_of_training_steps = 50000
   target_accuracy = 0.7
   target_false_activation_per_hour = 0.5
   ```

3. Run all cells. Colab will synthesize the phrase ~5000 times in
   different voices, train the model on T4 GPU, and produce an `.tflite`
   file + an `.onnx` file.

4. Download **both** files. Copy them to the hub at
   `/home/pi/openwakeword-models/`:
   ```bash
   scp ehi_claw.tflite ehi_claw.onnx pi@homeclaw-hub:/home/pi/openwakeword-models/
   ```

5. Update the systemd unit to preload the new model:
   ```bash
   sudo systemctl edit wyoming-openwakeword
   ```
   Add:
   ```
   [Service]
   ExecStart=
   ExecStart=/home/pi/wyoming-openwakeword/script/run \
       --uri tcp://0.0.0.0:10400 \
       --custom-model-dir /home/pi/openwakeword-models \
       --preload-model ehi_claw \
       --threshold 0.5
   ```
   Then:
   ```bash
   sudo systemctl restart wyoming-openwakeword
   ```

6. Tell the satellite to use the new wake word:
   ```bash
   sudo systemctl edit wyoming-satellite
   ```
   Change `--wake-word-name ok_nabu` to `--wake-word-name ehi_claw`.
   Restart:
   ```bash
   sudo systemctl restart wyoming-satellite
   ```

7. Test: say "Ehi Claw". The LED should pulse blue.

## The baseline will have false positives

The default-trained model hears "Ehi Claw" but also hears:
- "Hey cloud"
- "Hai voglia"
- "Hai visto" (in some dialects)
- TV ambient speech with similar sibilance

This is normal. Two fixes:

### Fix 1 — Raise threshold

In `wyoming-openwakeword` service, change `--threshold 0.5` to
`--threshold 0.6` or `0.7`. Higher = stricter = fewer false positives
but also more false negatives (it misses real "Ehi Claw" utterances).
Find your sweet spot over a week of use.

### Fix 2 — Fine-tune with your voice (big win)

The model ships knowing "Ehi Claw" said by many voices. It doesn't know
YOUR voice, which is the one saying it 95% of the time at your house.
Adding 30–50 recordings of you + people in the house saying it (plus
30–50 negative examples of words it wrongly triggered on) cuts false
positive rate by 80%+ in my testing.

The fine-tune procedure is documented in the openWakeWord README:
https://github.com/dscripka/openWakeWord/blob/main/docs/custom_models.md

### Collecting real-world data

The `wyoming-satellite` service supports `--debug-recording-dir`. Enable
it for the first week. It saves every triggered audio chunk to disk.
Review periodically:

```bash
cd /home/pi/homeclaw-debug
ls -lh          # recent triggers
aplay 2026-04-24_14-32-01.wav   # listen to one
```

Sort triggers into:
- `positive/` — you said "Ehi Claw", correct trigger
- `negative/` — you didn't say it, false alarm

Feed both folders into the fine-tune notebook. Result: a wake word that
knows YOUR voice against YOUR acoustic environment.

## Disable debug recording in production

Debug recording leaks audio to disk. Turn it off once fine-tuning is done:

```bash
sudo systemctl edit wyoming-satellite
# remove the --debug-recording-dir flag
sudo systemctl restart wyoming-satellite
sudo rm -rf /home/pi/homeclaw-debug
```

## Common pitfalls

- **Wake word model in wrong format.** The `.tflite` file is what
  openWakeWord loads; the `.onnx` file is for porting to other frameworks.
  Keep both — if you ever move to microWakeWord on ESP32, you'll want
  the `.onnx` to retrain for the int8 quantized pipeline there.
- **Phonetic collisions with Italian.** "Ehi" + "Claw" is a decent choice
  because "Claw" has no close phonetic neighbor in Italian. Avoid
  short monosyllabic wake words ("Claw" alone) — too many false positives
  in daily speech.
- **Too-accented training voice.** The Colab notebook uses
  multi-language TTS to synthesize training data. If your wake word
  recognition is poor, re-run with a wider `voice_seed_count`.
