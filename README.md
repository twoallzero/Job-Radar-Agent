# Job Radar Agent

매일 아침 채용 공고를 수집·분석해 텔레그램으로 발송하는 자동화 에이전트.

## 구조

```
Job-Radar-Agent/
├── main.py                  # 오케스트레이터
├── config.py                # 설정 (키워드, 점수 가중치)
├── agents/
│   ├── job_collector.py     # STEP 1: 수집 (inthiswork, 아이컨카페, LinkedIn, 잡알리오)
│   ├── job_analyst.py       # STEP 2: 분석 (Claude API, Top 10 선정, 커버레터 초안)
│   └── job_reporter.py      # STEP 3: 텔레그램 발송
├── reports/
│   ├── collected/           # 수집 원본 JSON
│   └── analysis/            # 분석 보고서 (.md)
├── drafts/                  # 커버레터 초안 (.md)
├── logs/                    # 실행 로그
└── templates/
    └── design.md            # 텔레그램 카드 템플릿
```

## 설치

```bash
pip install -r requirements.txt
cp .env.example .env
# .env 파일에 키 입력
```

## .env 설정

```
ANTHROPIC_API_KEY=sk-ant-...
TELEGRAM_BOT_TOKEN=...      # @BotFather에서 발급
TELEGRAM_CHAT_ID=...        # 채널/그룹 ID (음수값)
```

### 텔레그램 봇 만들기 (처음인 경우)
1. 텔레그램에서 `@BotFather` 검색
2. `/newbot` → 봇 이름·username 설정 → **BOT_TOKEN** 발급
3. 원하는 채널/그룹에 봇 추가 (관리자 권한)
4. `https://api.telegram.org/bot<TOKEN>/getUpdates` 접속 → `chat.id` 확인

## 실행

```bash
# 수동 실행
python main.py

# cron 자동화 (매일 09:00)
bash setup_cron.sh
```

<img width="723" height="1478" alt="preview" src="https://github.com/user-attachments/assets/841cd113-3b16-4e20-b9fa-f2f3dc23eafa" />


## 점수 기준

| 조건 | 점수 |
|------|------|
| 마감 7일 이내 | +3 |
| 내 스택 매칭 1개당 | +2 |
| 대기업/유니콘 | +1 |
| 근무지 서울 | +1 |
