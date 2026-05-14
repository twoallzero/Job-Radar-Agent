"""텔레그램 양방향 봇 — 롱 폴링으로 명령을 수신하고 파이프라인을 실행한다."""
import logging
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

import sent_tracker
from agents import job_collector, job_analyst, job_reporter
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("bot")

API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
_running_lock = threading.Lock()  # 동시 실행 방지


# ── Telegram 헬퍼 ─────────────────────────────────────────────────────────────

def send(text: str, parse_mode: str = "HTML") -> None:
    try:
        requests.post(
            f"{API}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text,
                  "parse_mode": parse_mode, "disable_web_page_preview": True},
            timeout=10,
        )
    except Exception as e:
        logger.error(f"발송 실패: {e}")


def get_updates(offset: int) -> list[dict]:
    try:
        resp = requests.get(
            f"{API}/getUpdates",
            params={"offset": offset, "timeout": 30, "allowed_updates": ["message"]},
            timeout=40,
        )
        return resp.json().get("result", [])
    except Exception:
        return []


# ── 명령어 핸들러 ─────────────────────────────────────────────────────────────

def handle_run():
    if not _running_lock.acquire(blocking=False):
        send("⚙️ 이미 실행 중입니다. 잠시 후 다시 시도해주세요.")
        return

    def _task():
        try:
            send("🔍 수집 시작합니다...")
            start = time.time()

            jobs = job_collector.run()
            new_jobs = sent_tracker.filter_new(jobs)
            send(f"✅ 수집 완료: 전체 <b>{len(jobs)}건</b> → 신규 <b>{len(new_jobs)}건</b>")

            if not new_jobs:
                send("📭 새로운 공고가 없습니다.")
                return

            send("🧠 분석 중...")
            result = job_analyst.run(new_jobs)
            send(f"✅ 분석 완료: Top <b>{len(result['top10'])}건</b> 선정")

            elapsed = int(time.time() - start)
            job_reporter.run(result, total_collected=len(new_jobs), elapsed=elapsed)
            sent_tracker.mark_sent(result.get("top10", []))

            send(f"🎉 완료! 총 소요: {elapsed}초")
        except Exception as e:
            send(f"❌ 오류 발생: {e}")
            logger.exception(e)
        finally:
            _running_lock.release()

    threading.Thread(target=_task, daemon=True).start()


def handle_status():
    log_dir = Path("./logs")
    logs = sorted(log_dir.glob("run_*.log"), reverse=True)
    if not logs:
        send("📭 실행 기록이 없습니다.")
        return

    latest = logs[0]
    lines = latest.read_text(encoding="utf-8").splitlines()

    # 핵심 줄만 추출
    key_lines = [l for l in lines if any(
        kw in l for kw in ["완료 |", "수집 완료", "분석 완료", "발송 완료", "치명적", "신규 공고"]
    )][-10:]

    date_str = latest.stem.replace("run_", "")
    msg = f"📋 <b>마지막 실행 ({date_str})</b>\n\n" + "\n".join(
        l.split("] ")[-1] for l in key_lines
    )
    send(msg)


def handle_report():
    report_dir = Path("./reports/analysis")
    reports = sorted(report_dir.glob("report_*.md"), reverse=True)
    if not reports:
        send("📭 분석 보고서가 없습니다.")
        return

    content = reports[0].read_text(encoding="utf-8")
    # 텔레그램 메시지 제한 4096자
    chunks = [content[i:i+3800] for i in range(0, min(len(content), 15200), 3800)]
    for chunk in chunks:
        send(f"<pre>{chunk}</pre>")


def handle_help():
    send(
        "🤖 <b>Job Radar 명령어</b>\n\n"
        "/실행 — 지금 바로 수집·분석·발송\n"
        "/현황 — 마지막 실행 결과 요약\n"
        "/보고서 — Top 10 분석 보고서\n"
        "/도움 — 명령어 목록"
    )


COMMANDS = {
    "/실행": handle_run,
    "/run": handle_run,
    "/현황": handle_status,
    "/status": handle_status,
    "/보고서": handle_report,
    "/report": handle_report,
    "/도움": handle_help,
    "/help": handle_help,
    "/start": handle_help,
}


# ── 폴링 루프 ─────────────────────────────────────────────────────────────────

def main():
    logger.info("Job Radar 봇 시작")
    send("🤖 Job Radar 봇이 시작됐습니다. /도움 으로 명령어를 확인하세요.")

    offset = 0
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text", "").strip()
            chat_id = str(msg.get("chat", {}).get("id", ""))

            # 등록된 chat_id만 허용
            if chat_id != str(TELEGRAM_CHAT_ID):
                continue

            # 명령어 앞부분 매칭 (/실행@botname 형태도 처리)
            cmd = text.split("@")[0].split(" ")[0].lower()
            handler = COMMANDS.get(cmd) or COMMANDS.get(text.split("@")[0].split(" ")[0])
            if handler:
                logger.info(f"명령어 수신: {text}")
                handler()
            elif text:
                send(f"❓ 알 수 없는 명령어: {text}\n/도움 으로 명령어를 확인하세요.")


if __name__ == "__main__":
    main()
