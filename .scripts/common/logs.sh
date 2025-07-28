#!/bin/sh

# == Constants
NC='\033[0m'  # color reset
BLUE='\033[0;34m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BOLD_ORANGE='\033[1;33m'
RED='\033[0;31m'
DARKGRAY='\033[1;30m'


function level_color()
{
    case "$1" in
        INFO)    echo "$BLUE";;
        WARNING) echo "$ORANGE";;
        ERROR)   echo "$RED";;
        SUCCESS) echo "$GREEN";;
        *)       echo "";;  # Unknown level
    esac
}

# == Functions
function log_info()    { log "INFO"    "$@"; }
function log_warning() { log "WARNING" "$@"; }
function log_error()   { log "ERROR"   "$@"; }
function log_success() { log "SUCCESS" "$@"; }


function log()
{
    local level="$1"
    local message_summary="$2"
    local message_details="${@:3}"

    local color=$(level_color "$level")
    if [ -z "$color" ]; then
        log "ERROR" "Undefined log level: $level"
        return 1
    fi
    local padding=" "
    local max_padding=8  # max_length_log_level + 1
    local padding_length=$(($max_padding - ${#level}))

    printf "[$color${level}$NC]%${padding_length}s${message_summary}\n" "$padding"
    if [ -z "$message_details" ]; then
        return
    fi
    for line in "$message_details"; do
        # (max_padding + 2) to take square brackets [] into account
        printf "%$(($max_padding + 2))s${line}\n" "$padding"
    done
}
