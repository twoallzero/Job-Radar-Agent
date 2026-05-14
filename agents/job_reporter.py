import logging
from datetime import datetime
from pathlib import Path

import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


def _send(html: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": html,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"발송 실패: {e}")
        return False


def _is_urgent(job: dict) -> bool:
    deadline_str = job.get("deadline", "")
    if not deadline_str:
        return False
    try:
        deadline = datetime.fromisoformat(deadline_str.replace(" ", "T"))
        return 0 <= (deadline - datetime.now()).days <= 3
    except ValueError:
        return False


def run(analysis_result: dict, total_collected: int, elapsed: int = 0) -> None:
    top10 = analysis_result.get("top10", [])
    draft_paths = analysis_result.get("draft_paths", [])

    if not top10:
        _send("📭 새로운 공고가 없습니다.")
        return

    # 요약
    urgent_count = sum(1 for j in top10 if _is_urgent(j))
    date_str = datetime.now().strftime("%Y-%m-%d")

    summary = f"""<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white; margin-bottom: 16px;">
  <h2 style="margin: 0 0 8px 0; font-size: 24px;">📊 Job Radar Daily</h2>
  <p style="margin: 0; font-size: 14px; opacity: 0.9;">채용 공고 일일 리포트</p>
  <div style="margin-top: 12px; font-size: 16px; font-weight: bold;">
    수집: <span style="color: #FFE082;">⚡{total_collected}건</span>
    → Top <span style="color: #81C784;">✨{len(top10)}건</span> 선정
  </div>
  <div style="margin-top: 8px; font-size: 13px;">⚠️ 마감 3일 이내: <span style="color: #FF5252;">{urgent_count}건</span></div>
</div>"""
    _send(summary)

    # 파스텔 색상 카드 (10개)
    colors = [
        {"bg": "#FFE5E5", "border": "#FF6B6B", "btn": "#FF6B6B", "text_color": "white"},
        {"bg": "#FFF5E5", "border": "#FFB366", "btn": "#FFB366", "text_color": "white"},
        {"bg": "#FFFCE5", "border": "#FFD93D", "btn": "#FFD93D", "text_color": "#333"},
        {"bg": "#E5F5FF", "border": "#4ECDC4", "btn": "#4ECDC4", "text_color": "white"},
        {"bg": "#E5FFE5", "border": "#81C784", "btn": "#81C784", "text_color": "white"},
        {"bg": "#F5E5FF", "border": "#BA68C8", "btn": "#BA68C8", "text_color": "white"},
        {"bg": "#FFE5F0", "border": "#F06292", "btn": "#F06292", "text_color": "white"},
        {"bg": "#E0F7FA", "border": "#00BCD4", "btn": "#00BCD4", "text_color": "white"},
        {"bg": "#F1F8E9", "border": "#CDDC39", "btn": "#CDDC39", "text_color": "#333"},
        {"bg": "#FFE8D6", "border": "#FF9800", "btn": "#FF9800", "text_color": "white"},
    ]

    for rank, job in enumerate(top10, 1):
        colors_set = colors[rank - 1]
        company = job.get("company", "미상")
        title = job.get("title", "")
        job_type = job.get("type", "")
        deadline = job.get("deadline", "미정")
        requirements = ", ".join(job.get("requirements", [])[:3]) or "상세 공고 참고"
        reason = job.get("reason", "")
        difficulty = job.get("difficulty", "중")
        score = job.get("_score", 0)
        url = job.get("url", "#")

        card = f"""<div style="background: {colors_set['bg']}; border-radius: 12px; padding: 16px; margin-bottom: 12px; border-left: 4px solid {colors_set['border']};">
  <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
    <div>
      <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: bold; color: #2C3E50;">[{rank}/10] {company}</h3>
      <p style="margin: 0; font-size: 16px; color: #34495E;">{title}</p>
    </div>
    <div style="background: white; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: {colors_set['border']};">
      {job_type}
    </div>
  </div>

  <div style="background: rgba(255,255,255,0.6); padding: 12px; border-radius: 8px; margin-bottom: 12px; font-size: 13px; color: #555;">
    <div style="margin-bottom: 6px;">📅 <b>마감:</b> {deadline}</div>
    <div style="margin-bottom: 6px;">🔧 <b>필수:</b> {requirements}</div>
    <div>⭐ <b>추천:</b> {reason}</div>
  </div>

  <div style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 12px; color: #888;">
      🎯 난이도: <span style="font-weight: bold; color: #E67E22;">{difficulty}</span> | 점수: {score}점
    </div>
    <a href="{url}" style="background: {colors_set['btn']}; color: {colors_set['text_color']}; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold;">
      공고보기 →
    </a>
  </div>
</div>"""
        _send(card)

    # 긴급 마감
    urgent_jobs = [j for j in top10 if _is_urgent(j)]
    if urgent_jobs:
        urgent_msg = """<div style="background: linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%); border-radius: 12px; padding: 16px; margin-bottom: 16px; color: white;">
  <h3 style="margin: 0 0 12px 0; font-size: 18px;">🚨 마감 3일 이내 긴급 공고</h3>
  <div style="font-size: 13px; line-height: 1.8;">"""
        for job in urgent_jobs[:3]:
            urgent_msg += f"""    • <b>{job.get('company', '미상')}</b> — {job.get('title', '')}<br>
    &nbsp;&nbsp;마감: {job.get('deadline', '미정')}<br><br>
"""
        urgent_msg += """  </div>
</div>"""
        _send(urgent_msg)

    # 커버레터 초안
    if draft_paths:
        draft_msg = """<div style="background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%); border-radius: 12px; padding: 16px; margin-bottom: 16px; color: white;">
  <h3 style="margin: 0 0 8px 0; font-size: 18px;">✍️ 지원 동기 초안 작성 완료</h3>
  <p style="margin: 8px 0; font-size: 13px; opacity: 0.95;">다음 공고들의 커버레터 초안이 생성되었습니다.</p>
  <div style="background: rgba(0,0,0,0.15); padding: 10px; border-radius: 6px; margin-top: 10px; font-size: 12px; font-family: monospace;">"""
        for path in draft_paths:
            draft_msg += f"    📄 {Path(path).name}<br>\n"
        draft_msg += """  </div>
</div>"""
        _send(draft_msg)

    # 푸터
    footer = f"""<div style="text-align: center; padding: 16px; background: #F8F9FA; border-radius: 12px; border-top: 2px solid #DDD; font-size: 12px; color: #666;">
  <p style="margin: 0 0 8px 0;">
    🤖 <b>Job Radar Agent</b> v2.0
  </p>
  <p style="margin: 0;">
    📅 {date_str} | ⏱️ {elapsed}초 소요
  </p>
</div>"""
    _send(footer)

    logger.info("텔레그램 발송 완료")
