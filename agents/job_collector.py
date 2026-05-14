import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from config import KEYWORDS

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}

OUTPUT_DIR = Path("./reports/collected")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _make_id(source: str, idx: int) -> str:
    date_str = datetime.now().strftime("%Y%m%d")
    return f"job_{date_str}_{source}_{idx:03d}"


# ── Source 1: inthiswork (Playwright) ──────────────────────────────────────────

def collect_inthiswork() -> list[dict]:
    source = "inthiswork"
    results = []
    logger.info(f"[{source}] 수집 시작 (Playwright 브라우저)")

    keywords_to_search = ["인턴", "신입", "데이터분석", "기획"]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            for search_keyword in keywords_to_search:
                try:
                    url = f"https://inthiswork.com/?s={requests.utils.quote(search_keyword)}"
                    logger.info(f"[{source}] 검색: {search_keyword} → {url}")

                    page.goto(url, wait_until="domcontentloaded")
                    time.sleep(1)

                    soup = BeautifulSoup(page.content(), "html.parser")
                    links = soup.find_all("h2", class_="entry-title")
                    logger.debug(f"[{source}] {search_keyword}: find_all('h2') 결과 {len(links)}개")

                    for idx, h2 in enumerate(links[:15]):
                        try:
                            a_tag = h2.find("a")
                            if not a_tag:
                                logger.debug(f"[{source}] h2[{idx}]: a 태그 없음")
                                continue

                            title = a_tag.get_text(strip=True)
                            url_job = a_tag.get("href", "")
                            logger.debug(f"[{source}] h2[{idx}]: title='{title}' | url={url_job}")

                            # 키워드 필터
                            if not any(kw in title for kw in KEYWORDS):
                                logger.debug(f"[{source}] 필터 제외: '{title}'")
                                continue

                            company = title.split("｜")[0].strip() if "｜" in title else ""
                            job_title = title.split("｜")[1].strip() if "｜" in title else title

                            job = {
                                "id": _make_id(source, len(results) + 1),
                                "source": source,
                                "company": company,
                                "title": job_title,
                                "type": "인턴" if "인턴" in title else "신입",
                                "deadline": "",
                                "requirements": [],
                                "preferred": [],
                                "url": url_job,
                                "collected_at": datetime.now().isoformat(),
                            }
                            results.append(job)
                            logger.debug(f"[{source}] 추가됨: {job['title']}")
                        except Exception as e:
                            logger.warning(f"[{source}] 파싱 오류: {e}")

                except Exception as e:
                    logger.warning(f"[{source}] '{search_keyword}' 실패: {e}")

            page.close()
            context.close()
            browser.close()

    except Exception as e:
        logger.error(f"[{source}] 오류: {e}")

    logger.info(f"[{source}] 수집 완료: {len(results)}건")
    return results


# ── Source 2: 아이컨 카페 (공개 게시판) ────────────────────────────────────────

def collect_naver_cafe() -> list[dict]:
    source = "navercafe_iloveconsulting"
    results = []
    logger.info(f"[{source}] 수집 시작 (공개 게시판만)")

    search_url = (
        f"https://cafe.naver.com/ArticleSearchList.nhn"
        f"?search.clubid=10050146&search.searchBy=0&search.query="
    )

    for keyword in ["인턴", "신입채용", "채용공고"]:
        try:
            url = search_url + requests.utils.quote(keyword)
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "lxml")
            items = soup.select(".article-board tbody tr, .board-list li")

            for item in items[:10]:
                try:
                    title_el = item.select_one("a.article, .article-title a, td.td_article a")
                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    if not any(kw in title for kw in KEYWORDS):
                        continue

                    href = title_el.get("href", "")
                    link = f"https://cafe.naver.com{href}" if href.startswith("/") else href

                    results.append({
                        "id": _make_id(source, len(results) + 1),
                        "source": source,
                        "company": "",
                        "title": title,
                        "type": "인턴" if "인턴" in title else "신입",
                        "deadline": "",
                        "requirements": [],
                        "preferred": [],
                        "url": link,
                        "collected_at": datetime.now().isoformat(),
                    })
                except Exception as e:
                    logger.warning(f"[{source}] 파싱 오류: {e}")

            time.sleep(1)
        except Exception as e:
            logger.warning(f"[{source}] '{keyword}' 검색 실패: {e}")

    logger.info(f"[{source}] 수집 완료: {len(results)}건")
    return results


# ── Source 3: 링크드인 ────────────────────────────────────────────────────────

def collect_linkedin() -> list[dict]:
    source = "linkedin"
    results = []
    logger.info(f"[{source}] 수집 시작")

    search_terms = ["데이터분석 인턴", "기획 신입", "BA analyst intern"]
    for term in search_terms:
        try:
            url = (
                "https://www.linkedin.com/jobs/search/"
                f"?keywords={requests.utils.quote(term)}&location=Korea"
            )
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code in (429, 999):
                logger.warning(f"[{source}] 레이트 리미트, 스킵")
                break

            soup = BeautifulSoup(resp.text, "lxml")
            cards = soup.select(".job-search-card, .base-card")

            for card in cards[:10]:
                try:
                    title_el = card.select_one("h3.base-search-card__title, h3")
                    company_el = card.select_one("h4.base-search-card__subtitle, h4")
                    link_el = card.select_one("a.base-card__full-link, a")

                    if not title_el:
                        continue

                    title = title_el.get_text(strip=True)
                    company = company_el.get_text(strip=True) if company_el else ""
                    link = link_el.get("href", "") if link_el else ""

                    if not any(kw in title for kw in KEYWORDS):
                        continue

                    results.append({
                        "id": _make_id(source, len(results) + 1),
                        "source": source,
                        "company": company,
                        "title": title,
                        "type": "인턴" if "인턴" in title.lower() else "신입",
                        "deadline": "",
                        "requirements": [],
                        "preferred": [],
                        "url": link,
                        "collected_at": datetime.now().isoformat(),
                    })
                except Exception as e:
                    logger.warning(f"[{source}] 파싱 오류: {e}")

            time.sleep(2)
        except Exception as e:
            logger.warning(f"[{source}] 검색 실패: {e}")

    logger.info(f"[{source}] 수집 완료: {len(results)}건")
    return results


# ── Source 4: 잡알리오 (공공기관) ─────────────────────────────────────────────

def collect_jaballio() -> list[dict]:
    source = "jaballio"
    results = []
    logger.info(f"[{source}] 수집 시작")

    try:
        url = "https://job.alio.go.kr/recruit.do?method=list&type=L"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "lxml")
        rows = soup.select("table.tbl_list tbody tr, .recruit-list li")

        for idx, row in enumerate(rows[:20]):
            try:
                title_el = row.select_one("td.title a, .title a, a")
                company_el = row.select_one("td.organ, .organ")
                deadline_el = row.select_one("td.date, .date")

                if not title_el:
                    continue

                title = title_el.get_text(strip=True)
                if not any(kw in title for kw in KEYWORDS):
                    continue

                href = title_el.get("href", "")
                link = f"https://job.alio.go.kr{href}" if href.startswith("/") else href

                results.append({
                    "id": _make_id(source, len(results) + 1),
                    "source": source,
                    "company": company_el.get_text(strip=True) if company_el else "",
                    "title": title,
                    "type": "인턴" if "인턴" in title else "신입",
                    "deadline": deadline_el.get_text(strip=True) if deadline_el else "",
                    "requirements": [],
                    "preferred": [],
                    "url": link,
                    "collected_at": datetime.now().isoformat(),
                })
            except Exception as e:
                logger.warning(f"[{source}] 파싱 오류: {e}")

    except Exception as e:
        logger.warning(f"[{source}] 접근 실패: {e}")

    logger.info(f"[{source}] 수집 완료: {len(results)}건")
    return results


# ── 스킬 추출 헬퍼 ────────────────────────────────────────────────────────────

SKILL_KEYWORDS = [
    "Python", "SQL", "R", "Excel", "PowerPoint", "PPT", "Tableau", "Power BI",
    "통계", "머신러닝", "딥러닝", "데이터분석", "SPSS", "SAS", "Hadoop", "Spark",
    "AWS", "GCP", "Azure", "Git", "Java", "JavaScript", "영어", "TOEIC", "TOEFL",
]


def _extract_skills(text: str) -> list[str]:
    return [skill for skill in SKILL_KEYWORDS if skill.lower() in text.lower()]


# ── 메인 진입점 ───────────────────────────────────────────────────────────────

def run() -> list[dict]:
    # 기존 파일이 있으면 먼저 시도
    date_str = datetime.now().strftime("%Y%m%d")
    out_path = OUTPUT_DIR / f"jobs_{date_str}.json"
    if out_path.exists():
        try:
            with open(out_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
                if existing and len(existing) > 0:
                    logger.info(f"기존 파일 로드: {len(existing)}건")
                    return existing
        except Exception as e:
            logger.warning(f"기존 파일 로드 실패: {e}, 수집 재개...")

    all_jobs = []
    sources = [
        ("inthiswork", collect_inthiswork),
        ("navercafe", collect_naver_cafe),
        ("linkedin", collect_linkedin),
        ("jaballio", collect_jaballio),
    ]

    for name, func in sources:
        try:
            jobs = func()
            all_jobs.extend(jobs)
        except Exception as e:
            logger.error(f"[{name}] 치명적 오류: {e}")
            try:
                logger.info(f"[{name}] 재시도 중...")
                jobs = func()
                all_jobs.extend(jobs)
            except Exception as e2:
                logger.error(f"[{name}] 재시도 실패, 스킵: {e2}")

    # deduplicate by title+company
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = (job["title"], job["company"])
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    # save to file
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(unique_jobs, f, ensure_ascii=False, indent=2)

    logger.info(f"총 {len(unique_jobs)}건 수집 완료 → {out_path}")
    return unique_jobs
