#!/bin/bash
PROJECT_DIR="$HOME/Job-Radar-Agent"
PID_FILE="$PROJECT_DIR/logs/bot.pid"
LOG_FILE="$PROJECT_DIR/logs/bot.log"

mkdir -p "$PROJECT_DIR/logs"

if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
    echo "⚠️  봇이 이미 실행 중입니다. (PID: $(cat $PID_FILE))"
    exit 1
fi

cd "$PROJECT_DIR"
nohup ~/.pyenv/versions/3.11.8/bin/python3.11 bot.py >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "✅ 봇 시작 (PID: $!)"
echo "   로그: $LOG_FILE"
