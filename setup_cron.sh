#!/bin/bash
# 매일 오전 9시 자동 실행 cron 등록
# 실행: bash setup_cron.sh

PROJECT_DIR="$HOME/Job-Radar-Agent"
PYTHON=$(which python3)
LOG="$PROJECT_DIR/logs/cron.log"

CRON_JOB="0 9 * * * cd $PROJECT_DIR && $PYTHON main.py >> $LOG 2>&1"

# 기존 동일 job이 없을 때만 추가
(crontab -l 2>/dev/null | grep -v "Job-Radar-Agent"; echo "$CRON_JOB") | crontab -

echo "✅ cron 등록 완료:"
echo "   $CRON_JOB"
echo ""
echo "확인: crontab -l"
