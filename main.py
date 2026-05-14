import logging
import sys
import time
from datetime import datetime
from pathlib import Path

from agents import job_collector, job_analyst, job_reporter
import sent_tracker

LOG_DIR = Path("./logs")
LOG_DIR.mkdir(exist_ok=True)


def setup_logging():
    date_str = datetime.now().strftime("%Y%m%d")
    log_path = LOG_DIR / f"run_{date_str}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return log_path


def main():
    log_path = setup_logging()
    logger = logging.getLogger("main")
    start = time.time()

    logger.info("=" * 60)
    logger.info(f"Job Radar Agent 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # ── STEP 1: 수집 ──────────────────────────────────────────────
    logger.info("\n[STEP 1] job-collector 시작")
    step1_start = time.time()
    try:
        jobs = job_collector.run()
        step1_elapsed = time.time() - step1_start
        logger.info(f"[STEP 1] 완료 | 수집: {len(jobs)}건 | 소요: {step1_elapsed:.1f}s | 에러: 없음")
    except Exception as e:
        logger.error(f"[STEP 1] 치명적 실패: {e}")
        jobs = []

    # 이미 발송한 공고 제거
    jobs = sent_tracker.filter_new(jobs)
    logger.info(f"[STEP 1] 신규 공고: {len(jobs)}건 (중복 제거 후)")

    if not jobs:
        logger.warning("[STEP 1] 신규 공고 없음. 이후 단계 스킵.")

    # ── STEP 2: 분석 ──────────────────────────────────────────────
    logger.info("\n[STEP 2] job-analyst 시작")
    step2_start = time.time()
    analysis_result = {"top10": [], "report_path": None, "draft_paths": []}
    try:
        analysis_result = job_analyst.run(jobs)
        step2_elapsed = time.time() - step2_start
        logger.info(
            f"[STEP 2] 완료 | Top {len(analysis_result['top10'])}건 선정"
            f" | 커버레터 {len(analysis_result['draft_paths'])}건"
            f" | 소요: {step2_elapsed:.1f}s | 에러: 없음"
        )
    except Exception as e:
        logger.error(f"[STEP 2] 치명적 실패: {e}")

    # ── STEP 3: 발송 ──────────────────────────────────────────────
    logger.info("\n[STEP 3] job-reporter 시작")
    step3_start = time.time()
    try:
        elapsed_so_far = int(time.time() - start)
        job_reporter.run(analysis_result, total_collected=len(jobs), elapsed=elapsed_so_far)
        step3_elapsed = time.time() - step3_start
        logger.info(f"[STEP 3] 완료 | 소요: {step3_elapsed:.1f}s | 에러: 없음")
        sent_tracker.mark_sent(analysis_result.get("top10", []))
    except Exception as e:
        logger.error(f"[STEP 3] 치명적 실패: {e}")

    # ── 최종 요약 ─────────────────────────────────────────────────
    total_elapsed = time.time() - start
    logger.info("\n" + "=" * 60)
    logger.info(f"전체 완료 | 총 소요: {total_elapsed:.1f}s | 로그: {log_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
