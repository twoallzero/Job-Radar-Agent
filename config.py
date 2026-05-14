import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

KEYWORDS = ["인턴", "신입", "BA", "RA", "DA", "AI", "기획", "데이터분석", "데이터 분석"]
MY_STACK = ["Python", "SQL", "영어", "Excel", "PPT"]

SCORING = {
    "deadline_urgent_days": 7,
    "deadline_urgent_score": 3,
    "stack_match_score": 2,
    "big_company_score": 1,
    "name_value_score": 1,
    "seoul_score": 1,
}

BIG_COMPANIES = [
    "삼성", "LG", "SK", "현대", "카카오", "네이버", "라인", "쿠팡", "배달의민족",
    "토스", "당근", "크래프톤", "넥슨", "엔씨소프트", "카카오뱅크", "케이뱅크",
    "하이브", "CJ", "롯데", "GS", "한화", "두산", "포스코", "KT", "SKT", "LGU+",
]

# 이력서에 쓰면 눈에 띄는 네임밸류 기업 (스타트업 포함)
NAME_VALUE_COMPANIES = [
    "맥킨지", "BCG", "베인", "딜로이트", "PwC", "KPMG", "EY", "삼일회계",
    "골드만삭스", "모건스탠리", "JP모건", "씨티", "한국투자", "미래에셋",
    "구글", "메타", "애플", "아마존", "마이크로소프트", "IBM", "오라클",
    "무신사", "야놀자", "직방", "비바리퍼블리카", "센드버드", "몰로코",
    "올리브영", "컬리", "오늘의집", "리디", "뤼이드", "스캐터랩",
    "현대자동차", "기아", "현대모비스", "삼성전자", "SK하이닉스",
]
