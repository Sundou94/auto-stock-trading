from __future__ import annotations

from sqlalchemy.orm import Session

from app.alpaca_client import get_daily_bars
from app.backtest.engine import run_backtest
from app.models import PerformanceSnapshot, Trader


def evaluate_all_traders(db: Session) -> list[PerformanceSnapshot]:
    """활성 트레이더 전원에 대해 심볼별 시세를 1회만 조회하여 백테스트 성과 스냅샷을 기록."""
    active = db.query(Trader).filter(Trader.is_active.is_(True)).all()
    bars_cache: dict[str, object] = {}
    snapshots = []
    for trader in active:
        if trader.symbol not in bars_cache:
            bars_cache[trader.symbol] = get_daily_bars(trader.symbol)
        price_df = bars_cache[trader.symbol]
        result = run_backtest(price_df, trader.strategy_type, trader.parameters, initial_cash=trader.cash)
        snapshot = PerformanceSnapshot(trader_id=trader.id, **result)
        db.add(snapshot)
        snapshots.append(snapshot)
    db.commit()
    for s in snapshots:
        db.refresh(s)
    return snapshots
