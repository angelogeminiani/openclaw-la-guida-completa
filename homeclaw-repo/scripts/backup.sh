#!/usr/bin/env bash
#
# HomeClaw backup script.
# Backs up the OpenClaw workspace + configuration + voice profiles to a
# timestamped tar.gz file. Intended to run periodically via cron or
# manually before major changes.
#
# Usage:
#   ./scripts/backup.sh [--dest DIR] [--keep N]
#
# --dest DIR   : destination directory (default: /home/pi/backups)
# --keep N     : keep the N most recent backups, delete older (default: 7)

set -euo pipefail

DEST="${HOME}/backups"
KEEP=7

# -----------------------------------------------------------------------------------------------------------------
#  h e l p e r s
# -----------------------------------------------------------------------------------------------------------------

log() { printf '\033[1;34m[backup]\033[0m %s\n' "$*"; }
err() { printf '\033[1;31m[error]\033[0m  %s\n' "$*" >&2; }

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dest) DEST="$2"; shift 2 ;;
            --keep) KEEP="$2"; shift 2 ;;
            -h|--help)
                sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
                exit 0
                ;;
            *) err "unknown arg: $1"; exit 2 ;;
        esac
    done
}

# -----------------------------------------------------------------------------------------------------------------
#  s t e p s
# -----------------------------------------------------------------------------------------------------------------

do_backup() {
    mkdir -p "$DEST"
    local timestamp; timestamp=$(date +%Y%m%d-%H%M%S)
    local archive="${DEST}/homeclaw-backup-${timestamp}.tar.gz"

    log "creating $archive"
    # Sources to back up. Skip venvs (reproducible), logs, and debug audio.
    tar -czf "$archive" \
        --exclude='.openclaw/.cache' \
        --exclude='.openclaw/*/venv' \
        --exclude='.openclaw/logs/*.log' \
        -C "$HOME" \
        .openclaw \
        homeclaw-repo/soul-templates \
        openwakeword-models \
        2>/dev/null || true

    # Voice profiles (if speaker-id is enabled).
    if [[ -d "${HOME}/.openclaw/speakers" ]]; then
        tar -rf "${archive%.gz}" \
            -C "$HOME" .openclaw/speakers 2>/dev/null || true
        gzip -f "${archive%.gz}"
    fi

    local size; size=$(du -h "$archive" | cut -f1)
    log "backup complete: ${archive} (${size})"
}

rotate() {
    local count; count=$(find "$DEST" -maxdepth 1 -name 'homeclaw-backup-*.tar.gz' | wc -l)
    if (( count <= KEEP )); then
        log "no rotation needed ($count backups <= $KEEP keep limit)"
        return
    fi
    log "rotating old backups (keeping $KEEP most recent)"
    find "$DEST" -maxdepth 1 -name 'homeclaw-backup-*.tar.gz' \
        -printf '%T@ %p\n' | sort -rn | tail -n +$((KEEP + 1)) \
        | while read -r _ path; do
            log "  deleting $(basename "$path")"
            rm -f "$path"
        done
}

# -----------------------------------------------------------------------------------------------------------------
#  m a i n
# -----------------------------------------------------------------------------------------------------------------

main() {
    parse_args "$@"
    do_backup
    rotate
    log "done."
    log ""
    log "Schedule via cron with:"
    log "  crontab -e"
    log "  0 3 * * 0   /home/pi/homeclaw-repo/scripts/backup.sh"
    log "(weekly, 3am Sunday)"
}

main "$@"
