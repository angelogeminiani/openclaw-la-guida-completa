#!/usr/bin/env bash
#
# HomeClaw diagnostic script.
# Runs a checklist against the local install and prints a pass/fail
# report. Safe to run anytime; performs no changes.
#
# Usage:
#   ./scripts/doctor.sh [--verbose]

set -uo pipefail        # NOT -e: we want to keep checking after a failure

VERBOSE=0
[[ "${1:-}" == "--verbose" || "${1:-}" == "-v" ]] && VERBOSE=1

# -----------------------------------------------------------------------------------------------------------------
#  h e l p e r s
# -----------------------------------------------------------------------------------------------------------------

PASS=0
FAIL=0
WARN=0

pass() { printf '\033[1;32m[PASS]\033[0m %s\n' "$*"; PASS=$((PASS+1)); }
fail() { printf '\033[1;31m[FAIL]\033[0m %s\n' "$*"; FAIL=$((FAIL+1)); }
warn() { printf '\033[1;33m[WARN]\033[0m %s\n' "$*"; WARN=$((WARN+1)); }
info() { [[ $VERBOSE -eq 1 ]] && printf '       %s\n' "$*"; return 0; }
hdr()  { printf '\n\033[1;36m== %s ==\033[0m\n' "$*"; }

check_service() {
    local svc="$1"
    if systemctl is-active --quiet "$svc"; then
        pass "$svc is active"
        info "$(systemctl show -p ActiveEnterTimestamp "$svc" | cut -d= -f2)"
    else
        fail "$svc is NOT active"
        info "  try: journalctl -u $svc -n 20 --no-pager"
    fi
}

check_port() {
    local port="$1" label="$2"
    if ss -ltn "sport = :$port" | grep -q ":$port"; then
        pass "$label listening on :$port"
    else
        fail "$label NOT listening on :$port"
    fi
}

check_file() {
    local path="$1" label="$2"
    if [[ -f "$path" ]]; then
        pass "$label present: $path"
    else
        fail "$label missing: $path"
    fi
}

check_command() {
    local cmd="$1" label="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        pass "$label command available: $cmd"
    else
        fail "$label command missing: $cmd"
    fi
}

# -----------------------------------------------------------------------------------------------------------------
#  c h e c k s
# -----------------------------------------------------------------------------------------------------------------

check_os() {
    hdr "OS and kernel"
    if grep -q 'bookworm' /etc/os-release 2>/dev/null; then
        pass "Raspberry Pi OS Bookworm detected"
    else
        warn "Not Raspberry Pi OS Bookworm — untested"
    fi
    local arch; arch=$(uname -m)
    if [[ "$arch" == "aarch64" ]]; then
        pass "64-bit kernel ($arch)"
    else
        fail "Kernel is $arch — HomeClaw requires 64-bit (aarch64)"
    fi
}

check_audio() {
    hdr "Audio hardware"
    check_command arecord "ALSA arecord"
    check_command aplay "ALSA aplay"
    if arecord -L 2>/dev/null | grep -q 'ArrayUAC10\|plughw:CARD='; then
        pass "Capture device found"
        info "$(arecord -L | grep 'plughw:' | head -3)"
    else
        fail "No usable capture device in 'arecord -L'"
    fi
    if aplay -L 2>/dev/null | grep -q 'plughw:CARD=\|default:CARD='; then
        pass "Playback device found"
    else
        warn "No USB/HDMI playback device in 'aplay -L'"
    fi
}

check_hailo() {
    hdr "Hailo NPU (optional, Tier B)"
    if ! command -v hailortcli >/dev/null 2>&1; then
        warn "hailortcli not installed — Tier A install or Hailo driver missing"
        return
    fi
    if hailortcli fw-control identify 2>/dev/null | grep -q 'HAILO10H'; then
        pass "Hailo-10H detected"
    elif hailortcli fw-control identify 2>/dev/null | grep -q 'HAILO8'; then
        pass "Hailo-8/8L detected"
    else
        fail "Hailo tool present but device not responding"
        info "  try: dmesg | grep -i hailo"
    fi
}

check_services() {
    hdr "Systemd services"
    check_service wyoming-openwakeword
    check_service wyoming-faster-whisper
    check_service wyoming-piper
    check_service wyoming-satellite
    check_service homeclaw-bridge
    if systemctl list-unit-files | grep -q homeclaw-led-feedback; then
        check_service homeclaw-led-feedback
    else
        info "LED feedback service not installed (optional)"
    fi
}

check_ports() {
    hdr "Network ports"
    check_port 10400 "wyoming-openwakeword"
    check_port 10300 "wyoming-faster-whisper"
    check_port 10200 "wyoming-piper"
    check_port 10700 "wyoming-satellite"
    if ss -ltn "sport = :18789" | grep -q ':18789'; then
        pass "OpenClaw gateway listening on :18789"
    else
        fail "OpenClaw gateway NOT listening on :18789 — is openclaw running?"
    fi
}

check_configs() {
    hdr "Agent config files"
    local ws="$HOME/.openclaw/homeclaw-workspace"
    check_file "$ws/SOUL.md" "SOUL.md"
    check_file "$ws/IDENTITY.md" "IDENTITY.md"
    check_file "$ws/TOOLS.md" "TOOLS.md"
}

check_power() {
    hdr "Power and thermal"
    if [[ -r /sys/firmware/devicetree/base/model ]]; then
        local model; model=$(tr -d '\0' < /sys/firmware/devicetree/base/model)
        info "Model: $model"
    fi
    if command -v vcgencmd >/dev/null 2>&1; then
        local throttled; throttled=$(vcgencmd get_throttled | cut -d= -f2)
        if [[ "$throttled" == "0x0" ]]; then
            pass "No throttling events reported"
        else
            warn "Throttling detected (get_throttled=$throttled). Check PSU."
        fi
        local temp; temp=$(vcgencmd measure_temp | grep -o '[0-9.]*')
        info "SoC temp: ${temp}°C"
        if (( $(echo "$temp > 80" | bc -l 2>/dev/null) )); then
            warn "Temperature above 80°C; check cooling"
        fi
    fi
}

check_disk() {
    hdr "Disk space"
    local used; used=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    if [[ "$used" -lt 80 ]]; then
        pass "Disk usage ${used}% (/)"
    else
        warn "Disk usage ${used}% — consider cleanup"
    fi
}

# -----------------------------------------------------------------------------------------------------------------
#  m a i n
# -----------------------------------------------------------------------------------------------------------------

main() {
    printf '\033[1mHomeClaw doctor\033[0m (verbose=%d)\n' "$VERBOSE"
    check_os
    check_audio
    check_hailo
    check_services
    check_ports
    check_configs
    check_power
    check_disk

    hdr "Summary"
    printf 'PASS: %d   WARN: %d   FAIL: %d\n' "$PASS" "$WARN" "$FAIL"
    if [[ $FAIL -gt 0 ]]; then
        printf '\n\033[1;31mStatus: UNHEALTHY\033[0m — fix FAILs above.\n'
        exit 1
    elif [[ $WARN -gt 0 ]]; then
        printf '\n\033[1;33mStatus: DEGRADED\033[0m — review WARNings.\n'
        exit 0
    else
        printf '\n\033[1;32mStatus: HEALTHY\033[0m\n'
        exit 0
    fi
}

main
