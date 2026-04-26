#!/usr/bin/env bash
#
# HomeClaw Tier B installer.
# Installs the Wyoming stack (openWakeWord, faster-whisper, Piper, satellite)
# and the HomeClaw bridge + LED feedback service on a fresh Raspberry Pi OS
# Bookworm 64-bit. Assumes OpenClaw is already installed and reachable on
# ws://127.0.0.1:18789.
#
# Usage:
#   sudo ./scripts/install-tier-b.sh [--skip-hailo] [--dry-run]
#
# --skip-hailo  : do not attempt to verify Hailo driver (Tier A install)
# --dry-run     : print commands without executing them
#
# Re-runnable: the script is idempotent; existing venvs/services are skipped.

set -euo pipefail
IFS=$'\n\t'

# -----------------------------------------------------------------------------------------------------------------
#  c o n s t a n t s
# -----------------------------------------------------------------------------------------------------------------

readonly REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly USER_NAME="${SUDO_USER:-pi}"
readonly USER_HOME="$(getent passwd "$USER_NAME" | cut -d: -f6)"
readonly WYOMING_REPOS=(
    "wyoming-openwakeword"
    "wyoming-faster-whisper"
    "wyoming-piper"
    "wyoming-satellite"
)

SKIP_HAILO=0
DRY_RUN=0

# -----------------------------------------------------------------------------------------------------------------
#  h e l p e r s
# -----------------------------------------------------------------------------------------------------------------

log()  { printf '\033[1;34m[install]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[warn]\033[0m    %s\n' "$*"; }
err()  { printf '\033[1;31m[error]\033[0m   %s\n' "$*" >&2; }

run() {
    # run <cmd...>  — respect --dry-run
    if [[ $DRY_RUN -eq 1 ]]; then
        printf '    [dry-run] %s\n' "$*"
    else
        "$@"
    fi
}

run_user() {
    # run_user <cmd...>  — run as the non-root owner user
    if [[ $DRY_RUN -eq 1 ]]; then
        printf '    [dry-run] (as %s) %s\n' "$USER_NAME" "$*"
    else
        sudo -u "$USER_NAME" -H bash -c "$*"
    fi
}

require_root() {
    if [[ $EUID -ne 0 ]]; then
        err "this script must be run as root (use sudo)"
        exit 1
    fi
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --skip-hailo) SKIP_HAILO=1 ;;
            --dry-run)    DRY_RUN=1 ;;
            -h|--help)
                sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
                exit 0
                ;;
            *)
                err "unknown arg: $1"; exit 2 ;;
        esac
        shift
    done
}

# -----------------------------------------------------------------------------------------------------------------
#  s t e p s
# -----------------------------------------------------------------------------------------------------------------

step_system_packages() {
    log "installing system packages via apt..."
    run apt-get update -qq
    run apt-get install -y --no-install-recommends \
        git python3-pip python3-venv python3-dev \
        alsa-utils portaudio19-dev libatlas-base-dev \
        ffmpeg build-essential \
        libasound2-dev libportaudio2
}

step_check_hailo() {
    if [[ $SKIP_HAILO -eq 1 ]]; then
        warn "skipping Hailo verification (--skip-hailo)"
        return
    fi
    if ! command -v hailortcli >/dev/null 2>&1; then
        warn "hailortcli not found; Tier A install, continuing without NPU"
        SKIP_HAILO=1
        return
    fi
    log "verifying Hailo NPU..."
    if hailortcli fw-control identify | grep -q 'HAILO10H\|HAILO8'; then
        log "Hailo NPU detected and responding"
    else
        err "Hailo NPU not responding. Re-run with --skip-hailo or fix the driver."
        exit 3
    fi
}

step_clone_wyoming() {
    log "cloning Wyoming repositories..."
    for repo in "${WYOMING_REPOS[@]}"; do
        local dest="${USER_HOME}/${repo}"
        if [[ -d "$dest" ]]; then
            log "  ${repo} already cloned; skipping"
            continue
        fi
        run_user "git clone --depth 1 https://github.com/rhasspy/${repo}.git ${dest}"
    done
}

step_setup_wyoming_venvs() {
    log "running script/setup for each Wyoming component..."
    for repo in "${WYOMING_REPOS[@]}"; do
        local dir="${USER_HOME}/${repo}"
        if [[ -f "${dir}/.venv/bin/activate" ]] || [[ -d "${dir}/venv" ]]; then
            log "  ${repo} venv already set up; skipping"
            continue
        fi
        run_user "cd ${dir} && script/setup"
    done
}

step_install_bridge() {
    log "setting up HomeClaw bridge venv..."
    local skill_dir="${REPO_DIR}/skill"
    if [[ ! -d "${skill_dir}/venv" ]]; then
        run_user "python3 -m venv ${skill_dir}/venv"
    fi
    run_user "${skill_dir}/venv/bin/pip install --upgrade pip"
    run_user "${skill_dir}/venv/bin/pip install -r ${skill_dir}/requirements.txt"
}

step_install_led_feedback() {
    log "setting up LED feedback venv..."
    local led_dir="${REPO_DIR}/led-feedback"
    if [[ ! -d "${led_dir}/venv" ]]; then
        run_user "python3 -m venv ${led_dir}/venv"
    fi
    run_user "${led_dir}/venv/bin/pip install --upgrade pip"
    run_user "${led_dir}/venv/bin/pip install -r ${led_dir}/requirements.txt"
}

step_install_systemd() {
    log "installing systemd service files..."
    run cp "${REPO_DIR}/systemd/"*.service /etc/systemd/system/
    run systemctl daemon-reload
    log "services installed. Enable & start them with:"
    printf '    sudo systemctl enable --now \\\n'
    printf '        wyoming-openwakeword \\\n'
    printf '        wyoming-faster-whisper \\\n'
    printf '        wyoming-piper \\\n'
    printf '        wyoming-satellite \\\n'
    printf '        homeclaw-bridge \\\n'
    printf '        homeclaw-led-feedback\n'
}

step_create_dirs() {
    log "creating runtime directories..."
    run_user "mkdir -p ${USER_HOME}/openwakeword-models"
    run_user "mkdir -p ${USER_HOME}/piper-voices"
    run_user "mkdir -p ${USER_HOME}/homeclaw-sounds"
    run_user "mkdir -p ${USER_HOME}/homeclaw-debug"
}

step_summary() {
    log "installation complete."
    printf '\nNext steps:\n'
    printf '  1. Drop your custom wake word .tflite into %s/openwakeword-models/\n' "$USER_HOME"
    printf '  2. Download a Piper voice:  piper --download-dir %s/piper-voices --voice it_IT-paola-medium\n' "$USER_HOME"
    printf '  3. Create the HomeClaw agent in OpenClaw (see README.md).\n'
    printf '  4. Copy soul-templates/*.md into ~/.openclaw/homeclaw-workspace/\n'
    printf '  5. Enable and start all services (command printed above).\n'
    printf '  6. Run ./scripts/doctor.sh to verify everything is healthy.\n'
}

# -----------------------------------------------------------------------------------------------------------------
#  m a i n
# -----------------------------------------------------------------------------------------------------------------

main() {
    parse_args "$@"
    require_root

    log "HomeClaw Tier B installer starting (user=${USER_NAME}, home=${USER_HOME})"
    step_system_packages
    step_check_hailo
    step_clone_wyoming
    step_setup_wyoming_venvs
    step_install_bridge
    step_install_led_feedback
    step_create_dirs
    step_install_systemd
    step_summary
}

main "$@"
