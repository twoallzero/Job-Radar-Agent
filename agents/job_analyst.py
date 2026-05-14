import json
import logging
from datetime import datetime
from pathlib import Path

from config import MY_STACK, SCORING, BIG_COMPANIES, NAME_VALUE_COMPANIES

logger = logging.getLogger(__name__)

ANALYSIS_DIR = Path("./reports/analysis")
DRAFTS_DIR = Path("./drafts")
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
DRAFTS_DIR.mkdir(parents=True, exist_ok=True)


# ── 점수 계산 ─────────────────────────────────────────────────────────────────

def _score(job: dict) -> float:
    score = 0.0

    # 마감 임박 +3
    deadline_str = job.get("deadline", "")
    if deadline_str:
        try:
            deadline = datetime.fromisoformat(deadline_str.replace(" ", "T"))
            days_left = (deadline - datetime.now()).days
            if 0 <= days_left <= SCORING["deadline_urgent_days"]:
                score += SCORING["deadline_urgent_score"]
        except ValueError:
            pass

    # 스택 매칭 +2 per match
    all_skills = job.get("requirements", []) + job.get("preferred", [])
    matched = [s for s in MY_STACK if any(s.lower() in skill.lower() for skill in all_skills)]
    score += len(matched) * SCORING["stack_match_score"]

    # 대기업/유니콘 +1
    company = job.get("company", "")
    if any(big in company for big in BIG_COMPANIES):
        score += SCORING["big_company_score"]

    # 네임밸류 기업 +1
    if any(nv in company for nv in NAME_VALUE_COMPANIES):
        score += SCORING["name_value_score"]

    # 서울 +1
    text = f"{job.get('title', '')} {company}"
    if "서울" in text or not any(
        city in text for city in ["부산", "대구", "인천", "광주", "대전", "울산"]
    ):
        score += SCORING["seoul_score"]

    job["_score"] = score
    job["_matched_stack"] = matched
    return score


# ── 규칙 기반 분석 ────────────────────────────────────────────────────────────

def _analyze(job: dict) -> dict:
    requirements = job.get("requirements", [])
    preferred = job.get("preferred", [])
    matched = job.get("_matched_stack", [])
    title = job.get("title", "")
    company = job.get("company", "미상")

    # 자격요건 요약
    if requirements:
        summary = ", ".join(requirements[:4])
    else:
        summary = "상세 요건은 공고 확인 필요"

    # 내가 충족하는 우대사항
    matched_preferred = [p for p in preferred if any(s.lower() in p.lower() for s in MY_STACK)]

    # 난이도: 매칭 스택 수 기준
    match_count = len(matched)
    if match_count >= 3:
        difficulty = "하"
    elif match_count >= 1:
        difficulty = "중"
    else:
        difficulty = "상"

    # 추천 이유
    if matched:
        reason = f"보유 스택({', '.join(matched[:2])}) 직접 활용 가능"
    elif any(big in company for big in BIG_COMPANIES):
        reason = "대기업/유니콘 — 경력에 유리"
    else:
        reason = "관련 직무 경험 쌓기에 적합"

    job["summary"] = summary
    job["matched_preferred"] = matched_preferred
    job["difficulty"] = difficulty
    job["reason"] = reason
    return job


# ── 커버레터 초안 (템플릿 기반) ───────────────────────────────────────────────

def _generate_cover_letter(job: dict, date_str: str, idx: int) -> Path:
    company = job.get("company", "회사명")
    title = job.get("title", "직무명")
    matched = job.get("_matched_stack", [])
    requirements = ", ".join(job.get("requirements", [])[:4]) or "데이터 분석"

    stack_sentence = (
        f"특히 {', '.join(matched[:2])}을(를) 실무에 적용한 경험이 있으며"
        if matched else
        "다양한 툴을 빠르게 학습하고 적용하는 능력을 갖추고 있으며"
    )

    content = f"""# {company} — {title} 지원 동기

{company}의 {title} 포지션에 지원하게 된 것은, 해당 직무가 요구하는 역량과 제가 준비해온 방향이 맞닿아 있다고 느꼈기 때문입니다.

저는 {', '.join(MY_STACK[:3])} 등의 스킬을 바탕으로 데이터를 분석하고 인사이트를 도출하는 데 관심을 기울여 왔습니다. {stack_sentence}, 이를 통해 {requirements} 등의 업무 요건에도 빠르게 기여할 수 있다고 생각합니다.

{company}가 추구하는 가치와 성장 방향에 공감하며, 주어진 역할에서 실질적인 성과를 만들어나가겠습니다. 부족한 부분은 빠른 학습과 적극적인 자세로 채워나가겠습니다.

---
*매칭 스택: {', '.join(matched) or '없음'} | 난이도: {job.get('difficulty', '중')} | 점수: {job.get('_score', 0)}점*
"""

    out_path = DRAFTS_DIR / f"cover_{date_str}_{idx:02d}_{company}.md"
    out_path.write_text(content, encoding="utf-8")
    logger.info(f"커버레터 저장: {out_path}")
    return out_path


# ── 분석 보고서 작성 ──────────────────────────────────────────────────────────

def _write_report(top10: list[dict], date_str: str) -> Path:
    lines = [
        f"# 채용공고 분석 보고서 — {date_str}",
        f"\n총 선정: Top {len(top10)}건\n",
        "---\n",
    ]

    for rank, job in enumerate(top10, 1):
        deadline = job.get("deadline") or "미정"
        matched = ", ".join(job.get("_matched_stack", [])) or "없음"

        lines += [
            f"## {rank}위. [{job.get('company', '미상')}] {job.get('title', '')}",
            f"- **출처**: {job.get('source', '')}",
            f"- **유형**: {job.get('type', '')}",
            f"- **마감**: {deadline}",
            f"- **점수**: {job.get('_score', 0)}점",
            f"- **난이도**: {job.get('difficulty', '중')}",
            f"- **자격요건 요약**: {job.get('summary', '')}",
            f"- **매칭 스택**: {matched}",
            f"- **추천 이유**: {job.get('reason', '')}",
            f"- **URL**: {job.get('url', '')}",
            "",
        ]

    out_path = ANALYSIS_DIR / f"report_{date_str}.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"분석 보고서 저장: {out_path}")
    return out_path


# ── 메인 진입점 ───────────────────────────────────────────────────────────────

def run(jobs: list[dict]) -> dict:
    date_str = datetime.now().strftime("%Y%m%d")

    if not jobs:
        logger.warning("분석할 공고 없음")
        return {"top10": [], "report_path": None, "draft_paths": []}

    for job in jobs:
        _score(job)
        _analyze(job)

    top10 = sorted(jobs, key=lambda x: x.get("_score", 0), reverse=True)[:10]
    report_path = _write_report(top10, date_str)

    # 커버레터: 난이도 하/중 + 매칭 2개 이상
    draft_paths = []
    eligible = [
        j for j in top10
        if j.get("difficulty") in ("하", "중") and len(j.get("_matched_stack", [])) >= 2
    ][:3]

    for idx, job in enumerate(eligible, 1):
        path = _generate_cover_letter(job, date_str, idx)
        draft_paths.append(str(path))

    logger.info(f"분석 완료: Top {len(top10)}건, 커버레터 {len(draft_paths)}건")
    return {
        "top10": top10,
        "report_path": str(report_path),
        "draft_paths": draft_paths,
    }
