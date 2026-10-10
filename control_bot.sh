#!/usr/bin/env bash
# Pause, resume, or check a running bot.
# Usage: ./control_bot.sh {pause|resume|status} PROFILE

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

PROFILE="$2"
if [ -z "$PROFILE" ] && [ -n "$1" ]; then
  echo "Which profile? Usage: $0 $1 PROFILE   (see: python3 main.py list)"
  exit 1
fi
PAUSE_FILE="data/$PROFILE/pause_bot.txt"

case "$1" in
  pause)
    mkdir -p "data/$PROFILE"
    touch "$PAUSE_FILE"
    echo "[✓] Bot for '$PROFILE' paused. It will pause after completing current job."
    ;;
  resume)
    rm -f "$PAUSE_FILE"
    echo "[✓] Bot for '$PROFILE' resumed."
    ;;
  status)
    if [ -f "$PAUSE_FILE" ]; then
      echo "[STATUS] Bot for '$PROFILE' is PAUSED"
    else
      echo "[STATUS] Bot for '$PROFILE' is RUNNING (or not started)"
    fi
    ;;
  *)
    echo "Usage: $0 {pause|resume|status} PROFILE"
    echo "  pause  - Pause bot after current job"
    echo "  resume - Resume bot operation"
    echo "  status - Check if bot is paused"
    exit 1
    ;;
esac
