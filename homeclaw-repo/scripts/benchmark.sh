#!/usr/bin/env bash
#
# HomeClaw end-to-end latency benchmark.
# Measures:
#   - Wake-word detection latency    (openWakeWord)
#   - STT latency                    (faster-whisper)
#   - Agent round-trip latency       (OpenClaw gateway)
#   - TTS latency                    (Piper)
#   - Total perceived latency        (sum)
#
# Uses a pre-recorded test utterance so results are comparable across runs
# and tiers (Tier A vs Tier B with/without NPU).
#
# Usage:
#   ./scripts/benchmark.sh [--runs N] [--utterance PATH.wav]

set -euo pipefail

RUNS=${1:-5}
UTTERANCE="${2:-/home/pi/homeclaw-sounds/test-utterance.wav}"

# -----------------------------------------------------------------------------------------------------------------
#  h e l p e r s
# -----------------------------------------------------------------------------------------------------------------

now_ms() {
    # Returns current epoch in milliseconds.
    echo $(($(date +%s%N) / 1000000))
}

time_ms_since() {
    local start=$1
    echo $(($(now_ms) - start))
}

# -----------------------------------------------------------------------------------------------------------------
#  c h e c k s
# -----------------------------------------------------------------------------------------------------------------

check_prereqs() {
    if [[ ! -f "$UTTERANCE" ]]; then
        echo "Test utterance not found: $UTTERANCE"
        echo "Generate one with:"
        echo "  echo 'Ehi Claw, che ore sono?' | piper \\"
        echo "      --model it_IT-paola-medium.onnx \\"
        echo "      --output_file $UTTERANCE"
        exit 1
    fi
    for svc in wyoming-faster-whisper wyoming-piper homeclaw-bridge; do
        if ! systemctl is-active --quiet "$svc"; then
            echo "Service $svc is not active; start it before benchmarking"
            exit 2
        fi
    done
}

# -----------------------------------------------------------------------------------------------------------------
#  b e n c h m a r k s
# -----------------------------------------------------------------------------------------------------------------

bench_stt() {
    # Send audio to wyoming-faster-whisper and measure transcription latency.
    local t0; t0=$(now_ms)
    python3 - <<'PY' "$UTTERANCE"
import asyncio, sys, wave
from wyoming.client import AsyncTcpClient
from wyoming.audio import AudioStart, AudioChunk, AudioStop
from wyoming.asr import Transcribe, Transcript

async def go(path):
    async with AsyncTcpClient('127.0.0.1', 10300) as c:
        await c.write_event(Transcribe(language='it').event())
        with wave.open(path, 'rb') as w:
            rate, width, channels = w.getframerate(), w.getsampwidth(), w.getnchannels()
            await c.write_event(AudioStart(rate=rate, width=width, channels=channels).event())
            while True:
                data = w.readframes(1024)
                if not data: break
                await c.write_event(AudioChunk(audio=data, rate=rate, width=width, channels=channels).event())
            await c.write_event(AudioStop().event())
        while True:
            ev = await c.read_event()
            if ev is None: break
            if Transcript.is_type(ev.type):
                t = Transcript.from_event(ev)
                print(t.text)
                return
asyncio.run(go(sys.argv[1]))
PY
    time_ms_since "$t0"
}

bench_tts() {
    local t0; t0=$(now_ms)
    python3 - <<'PY'
import asyncio
from wyoming.client import AsyncTcpClient
from wyoming.tts import Synthesize, SynthesizeVoice
from wyoming.audio import AudioStart, AudioStop

async def go():
    async with AsyncTcpClient('127.0.0.1', 10200) as c:
        await c.write_event(Synthesize(
            text='Sono le dieci e trenta.',
            voice=SynthesizeVoice(name='it_IT-paola-medium'),
        ).event())
        while True:
            ev = await c.read_event()
            if ev is None: break
            if AudioStart.is_type(ev.type):   return         # first audio frame == start
asyncio.run(go())
PY
    time_ms_since "$t0"
}

bench_agent() {
    # Assumes the bridge is running and connected to OpenClaw.
    # Uses the `openclaw` CLI to send a test message and measure reply time.
    local t0; t0=$(now_ms)
    openclaw agents send HomeClaw "Benchmark ping, rispondi solo con OK." \
        --channel voice --peer benchmark --timeout 8 >/dev/null
    time_ms_since "$t0"
}

# -----------------------------------------------------------------------------------------------------------------
#  m a i n
# -----------------------------------------------------------------------------------------------------------------

main() {
    check_prereqs

    printf 'HomeClaw benchmark — %d runs\n' "$RUNS"
    printf '%-10s  %-10s  %-10s  %-10s\n' "run" "STT(ms)" "Agent(ms)" "TTS(ms)"
    printf '%-10s  %-10s  %-10s  %-10s\n' "----" "-------" "--------" "-------"

    local sum_stt=0 sum_agent=0 sum_tts=0
    for ((i=1; i<=RUNS; i++)); do
        local t_stt   t_agent t_tts
        t_stt=$(bench_stt)
        t_agent=$(bench_agent)
        t_tts=$(bench_tts)
        printf '%-10d  %-10d  %-10d  %-10d\n' "$i" "$t_stt" "$t_agent" "$t_tts"
        sum_stt=$((sum_stt + t_stt))
        sum_agent=$((sum_agent + t_agent))
        sum_tts=$((sum_tts + t_tts))
    done

    local avg_stt=$((sum_stt / RUNS))
    local avg_agent=$((sum_agent / RUNS))
    local avg_tts=$((sum_tts / RUNS))
    local avg_total=$((avg_stt + avg_agent + avg_tts))

    printf '\n'
    printf 'AVG STT:   %d ms\n' "$avg_stt"
    printf 'AVG Agent: %d ms\n' "$avg_agent"
    printf 'AVG TTS:   %d ms\n' "$avg_tts"
    printf 'AVG Total: %d ms\n' "$avg_total"
    printf '\n'
    if (( avg_total < 2500 )); then
        printf '\033[1;32mTarget met: <2500ms perceived latency\033[0m\n'
    else
        printf '\033[1;33mOver budget: >2500ms. Consider Hailo NPU or smaller Whisper model.\033[0m\n'
    fi
}

main
