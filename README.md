# auto-stock-trading

AI를 활용한 주식 트레이딩 앱입니다.

유전알고리즘을 통해 1일(또는 지정 주기) 1회 알고리즘을 개선하는 아이디어에서 시작했습니다. 10명의 "트레이더"가 서로 다른 트레이딩 알고리즘으로 동시에 거래하고, 주기적으로 성과를 평가해 기준 수익률에 미달하는 트레이더는 우수 개체의 파라미터를 교차/변이시켜 새로운 트레이더로 교체합니다.

## 아키텍처

```
backend/   Python + FastAPI, SQLite, Alpaca Paper Trading 연동
├── app/strategies/   전략 템플릿 (이동평균 교차, RSI, 볼린저밴드, MACD, 모멘텀)
├── app/genetic/      유전알고리즘 엔진 (시딩 / 도태 / 교차·변이)
├── app/backtest/     전략 성과 계산 (수익률, 샤프비율, MDD, 승률)
├── app/api/          REST API 라우터
├── app/alpaca_client.py  Alpaca 시세/계좌/주문 연동
└── app/models.py     Trader, Trade, PerformanceSnapshot, EvolutionEvent

frontend/  React + TypeScript + Vite
├── 대시보드         트레이더 10명 카드 뷰 (도트 캐릭터, 수익률 랭킹)
├── 트레이더 상세     파라미터, 성과 지표, 매매 내역
├── 진화 히스토리     세대별 도태/교체 로그
└── 알고리즘 라이브러리  전략 템플릿 설명
```

## 실행 방법

### 1. 백엔드

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 이미 있다면 생략, ALPACA 키 채우기
uvicorn app.main:app --reload --port 8000
```

API 문서: http://localhost:8000/docs

### 2. 프론트엔드

```bash
cd frontend
npm install
npm run dev
```

http://localhost:5173 에서 확인. 백엔드가 8000번 포트에서 떠 있어야 합니다.

### 3. 초기 데이터 생성

대시보드의 "트레이더 10명 시딩" 버튼을 누르거나, API로 직접 호출:

```bash
curl -X POST http://localhost:8000/api/traders/seed
curl -X POST http://localhost:8000/api/evaluate   # Alpaca 시세로 백테스트 성과 평가
curl -X POST "http://localhost:8000/api/evolve?generation=1&min_return_threshold_pct=0"
```

## 환경 변수 (`backend/.env`)

```
ALPACA_API_KEY_ID=       # https://app.alpaca.markets 에서 Paper Trading 모드로 발급
ALPACA_API_SECRET_KEY=
ALPACA_BASE_URL=https://paper-api.alpaca.markets
DATABASE_URL=sqlite:///./trading.db
FRONTEND_ORIGIN=http://localhost:5173
```

`.env`는 `.gitignore`에 등록되어 있어 커밋되지 않습니다.

## 현재 상태 / 알려진 제약

- **거래 대상**: 미국 주식, Alpaca Paper Trading (모의투자) 연동. 실계좌 전환은 `ALPACA_BASE_URL`을 `https://api.alpaca.markets`로 바꾸고 실계좌 키를 발급받으면 됩니다.
- **핵심 로직 검증 완료**: 전략 5종 백테스트, DB 모델, 유전알고리즘 시딩/평가/도태/교차·변이 사이클, FastAPI 전체 API, React 대시보드 4개 화면 모두 로컬에서 실제 구동 확인했습니다.
- **미검증 영역**: 이 개발 환경의 아웃바운드 네트워크 정책상 Alpaca API(`paper-api.alpaca.markets`)로 직접 연결이 차단되어 있어, `/api/account`·`/api/evaluate`의 실제 Alpaca 연동은 이 세션에서 검증하지 못했습니다. 로컬 PC 또는 네트워크 제약이 없는 환경에서 실행하면 정상 동작할 것으로 예상됩니다.
- **아직 없는 기능**: 자동 스케줄러(주기적 평가/진화 실행), 실제 주문 체결(`submit_paper_order`) 연결, 로그인/멀티유저.

## 다음 단계 제안

1. APScheduler로 평가·진화 사이클 자동화 (예: 매일 장마감 후)
2. `/api/evaluate` 이후 각 트레이더의 신호에 따라 실제 페이퍼 주문 실행
3. 자산 곡선(equity curve) 차트 추가
4. 논문 기반 전략을 새 템플릿으로 추가하는 방식 정립
