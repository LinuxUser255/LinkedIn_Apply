#!/usr/bin/env bash
# Bot control script for pausing and resuming

case "$1" in
  pause)
    mkdir -p data
    touch data/pause_bot.txt
    echo "[✓] Bot paused. It will pause after completing current job."
    ;;
  resume)
    rm -f data/pause_bot.txt
    echo "[✓] Bot resumed."
    ;;
  status)
    if [ -f data/pause_bot.txt ]; then
      echo "[STATUS] Bot is PAUSED"
    else
      echo "[STATUS] Bot is RUNNING (or not started)"
    fi
    ;;
  *)
    echo "Usage: $0 {pause|resume|status}"
    echo "  pause  - Pause bot after current job"
    echo "  resume - Resume bot operation"
    echo "  status - Check if bot is paused"
    exit 1
    ;;
esac