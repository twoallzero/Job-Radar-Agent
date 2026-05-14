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

### 작동 사진
<img width="300" alt="preview" src="https://github.com/user-attachments/assets/81a46069-58c3-4859-82de-7d067ef7b707" />


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
