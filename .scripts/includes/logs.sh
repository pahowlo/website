#!/bin/sh

# == Constants
NC='\033[0m'  # color reset
BLUE='\033[0;34m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BOLD_ORANGE='\033[1;33m'
RED='\033[0;31m'
DARKGRAY='\033[1;30m'


level_color() {
    case "$1" in
        INFO)    echo "$BLUE";;
        WARNING) echo "$ORANGE";;
        ERROR)   echo "$RED";;
        SUCCESS) echo "$GREEN";;
        *)       echo "";;  # Unknown level
    esac
}

# == Functions
log_info()    { log "INFO"    "$@"; }
log_warning() { log "WARNING" "$@"; }
log_error()   { log "ERROR"   "$@"; }
log_success() { log "SUCCESS" "$@"; }


log() {
    (
        set -eu

        level="${1:-}"
        message_summary="${2:-}"
        message_details="${@:3}"

        color=$(level_color "$level")
        if [ -z "$color" ]; then
            log "ERROR" "Undefined log level: $level"
            return 1
        fi
        padding=" "
        max_padding=8  # max_length_log_level + 1
        padding_length=$(($max_padding - ${#level}))

        printf "[$color${level}$NC]%${padding_length}s${message_summary}\n" "$padding"
        if [ -z "$message_details" ]; then
            return
        fi
        for line in "$message_details"; do
            # (max_padding + 2) to take square brackets [] into account
            printf "%$(($max_padding + 2))s${line}\n" "$padding"
        done
    )
}
