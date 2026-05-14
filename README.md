# Job Radar Agent 🚀

매일 아침 한국 채용 공고를 수집·분석해 Telegram으로 발송하는 자동화 에이전트.

**특징:**
- ✅ 자동 수집: inthiswork.com에서 매일 58개 공고 수집
- ✅ 스마트 분석: 규칙 기반 점수 알고리즘으로 Top 10 추천
- ✅ Telegram 봇: 4가지 명령어로 실시간 제어
- ✅ 자동화: 매일 09:00에 cron 실행
- ✅ 중복 방지: 이미 발송한 공고 자동 제외

---

## 🏗️ 구조

```
Job-Radar-Agent/
├── main.py                     # 메인 오케스트레이션 (STEP 1-3)
├── bot.py                      # Telegram 봇 (24/7 폴링)
├── config.py                   # 설정 (키워드, 점수 가중치)
├── sent_tracker.py             # 중복 방지 추적
├── agents/
│   ├── job_collector.py        # [STEP 1] 웹 스크래핑 (Playwright)
│   ├── job_analyst.py          # [STEP 2] 분석 및 점수 (규칙 기반)
│   └── job_reporter.py         # [STEP 3] Telegram 발송
├── reports/
│   ├── collected/              # 수집한 원본 공고 (JSON)
│   └── analysis/               # 분석 보고서 (Markdown)
├── logs/                       # 실행 로그
├── setup_cron.sh               # cron 자동화 설치
├── start_bot.sh                # 봇 시작 스크립트
└── stop_bot.sh                 # 봇 중지 스크립트
```

---

## 🛠️ 설치

### 1. 저장소 클론
```bash
git clone https://github.com/twoallzero/Job-Radar-Agent.git
cd Job-Radar-Agent
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 설정
```bash
cp .env.example .env
```

`.env` 파일을 열어서 다음을 입력:
```
TELEGRAM_BOT_TOKEN=bot123456:ABCDEFGHIJKLMNOPQRSTUVWxyz...
TELEGRAM_CHAT_ID=-123456789
```

#### Telegram 설정 방법
1. Telegram에서 `@BotFather` 검색
2. `/newbot` 입력 → 봇 이름·username 입력 → **BOT_TOKEN** 받기
3. 봇을 원하는 채널/그룹에 추가 (관리자 권한 필요)
4. 아래 URL에 접속해서 `chat.id` 확인:
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```

---

## 🚀 실행

### 수동 실행 (즉시)
```bash
python main.py
```

### 자동 실행 (매일 09:00)
```bash
bash setup_cron.sh
```

이 명령이 cron job을 설정합니다.

### Telegram 봇 (24/7 백그라운드)
```bash
bash start_bot.sh    # 시작
bash stop_bot.sh     # 중지
```

---

## 💬 Telegram 명령어

Telegram에서 다음 명령어를 사용할 수 있습니다:

| 명령어 | 설명 |
|--------|------|
| `/실행` | 지금 바로 수집·분석·발송 실행 |
| `/현황` | 마지막 실행 결과 요약 |
| `/보고서` | 최신 Top 10 분석 보고서 |
| `/도움` | 명령어 목록 표시 |

---

## 📊 점수 알고리즘

각 공고는 다음 기준으로 점수가 매겨집니다:

| 조건 | 점수 |
|------|------|
| 마감 7일 이내 | +3 |
| 내 스택 매칭 1개당 | +2 |
| 대기업/유니콘 기업 | +1 |
| 근무지 서울 | +1 |

**난이도 판정:**
- `하`: 매칭 스택 3개 이상
- `중`: 매칭 스택 1-2개
- `상`: 매칭 스택 0개

### MY_STACK (설정 파일에서 변경 가능)
```python
MY_STACK = ["Python", "SQL", "영어", "Excel", "PPT"]
```

---

## 🔧 커스터마이징

### 키워드 변경 (어떤 공고를 수집할지)
`config.py`에서 `KEYWORDS` 수정:
```python
KEYWORDS = ["인턴", "신입", "데이터분석", "기획"]
```

### 점수 가중치 변경
`config.py`에서 `SCORING` 수정:
```python
SCORING = {
    "deadline_urgent_days": 7,
    "deadline_urgent_score": 3,
    "stack_match_score": 2,
    ...
}
```

### 대기업/네임밸류 기업 추가
`config.py`에서 `BIG_COMPANIES`, `NAME_VALUE_COMPANIES` 수정

---

## 📁 파일 설명

### `main.py`
메인 오케스트레이션 스크립트. 3단계 파이프라인 실행:
1. **STEP 1**: 공고 수집 (job_collector.py)
2. **STEP 2**: 분석 및 점수 (job_analyst.py)
3. **STEP 3**: Telegram 발송 (job_reporter.py)

### `bot.py`
Telegram 폴링 봇. 사용자 명령어를 받아 즉시 파이프라인 실행.

### `agents/job_collector.py`
**Playwright 기반 웹 스크래핑**
- inthiswork.com에서 4개 키워드로 검색
- 각 공고의 회사명, 직무명, URL, 유형 추출
- 캐시된 공고 파일에서 데이터 로드 (빠른 실행)

### `agents/job_analyst.py`
**규칙 기반 분석** (Claude API 없이)
- 각 공고에 점수 산정
- Top 10 선정
- 분석 보고서 (Markdown) 생성

### `agents/job_reporter.py`
**Telegram 메시지 발송**
- 요약 메시지 (수집·선정·긴급 공고 수)
- 10개 공고 카드 (색상 구분)
- 긴급 공고 알림 (3일 이내 마감)
- 푸터 (실행 시간)

### `sent_tracker.py`
**중복 방지 추적**
- `logs/sent_jobs.json`에 발송한 공고 URL 저장
- 다음 실행시 이미 발송한 공고 자동 제외

---

## 📊 출력 예시

### 콘솔 로그
```
2026-05-14 16:40:07 [INFO] main — [STEP 1] 완료 | 수집: 58건 | 소요: 25.6s
2026-05-14 16:40:07 [INFO] main — [STEP 1] 신규 공고: 48건 (중복 제거 후)
2026-05-14 16:40:07 [INFO] main — [STEP 2] 완료 | Top 10건 선정
2026-05-14 16:40:18 [INFO] agents.job_reporter — 텔레그램 발송 완료
```

### Telegram 메시지
- 📊 **Job Radar Daily** (요약)
- 🔴 **[1/10] 딜로이트 안진회계법인** (공고 카드들)
- 🚨 **마감 3일 이내 긴급 공고** (있을 때만)

---

## 🔄 자동화 설정 (macOS)

```bash
# cron 자동화 설정 (매일 09:00 실행)
bash setup_cron.sh

# 현재 cron 확인
crontab -l

# cron 제거
crontab -e  # 해당 줄 삭제
```

---

## 🐛 트러블슈팅

### Q: "새로운 공고가 없습니다" 계속 나옴
**A:** `logs/sent_jobs.json` 파일을 삭제하면 다음 실행에서 새로 발송됩니다.

### Q: Telegram 메시지가 안 옴
**A:** 
1. `.env` 파일에 `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` 확인
2. 봇이 채널/그룹의 관리자인지 확인
3. `python main.py` 실행해서 오류 메시지 확인

### Q: 수집되는 공고가 너무 적음
**A:** 
- `config.py`의 `KEYWORDS` 수정
- 다른 소스 (네이버카페, LinkedIn) 활성화 계획 중

---

## 📝 라이선스

MIT License

## 🤝 기여

버그 리포트, 피드백, Pull Request 환영합니다!

---

**Made with ❤️ using Python + Playwright + Telegram API**
