from __future__ import annotations

import numpy as np
import pandas as pd

from app.strategies.registry import STRATEGY_REGISTRY


def run_backtest(price_df: pd.DataFrame, strategy_type: str, params: dict, initial_cash: float = 10000.0) -> dict:
    """일봉 데이터로 롱-온리 전략을 시뮬레이션하고 성과 지표를 계산한다."""
    template = STRATEGY_REGISTRY[strategy_type]
    # 신호가 발생한 다음 날 체결된다고 가정(당일 종가 기준 신호로 당일 매매하는 룩어헤드 방지)
    positions = template.generate_signals(price_df, params).shift(1).fillna(0)
    daily_returns = price_df["close"].pct_change().fillna(0)
    strategy_returns = positions * daily_returns

    equity_curve = (1 + strategy_returns).cumprod() * initial_cash
    if len(equity_curve) == 0:
        return {
            "total_return_pct": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown_pct": 0.0,
            "win_rate_pct": 0.0,
            "portfolio_value": initial_cash,
        }

    total_return_pct = (equity_curve.iloc[-1] / initial_cash - 1) * 100

    daily_std = strategy_returns.std()
    sharpe_ratio = (strategy_returns.mean() / daily_std * np.sqrt(252)) if daily_std > 0 else 0.0

    running_max = equity_curve.cummax()
    drawdown = (equity_curve - running_max) / running_max
    max_drawdown_pct = drawdown.min() * 100

    active_days = strategy_returns[positions > 0]
    win_rate_pct = (active_days > 0).mean() * 100 if len(active_days) > 0 else 0.0

    return {
        "total_return_pct": round(float(total_return_pct), 2),
        "sharpe_ratio": round(float(sharpe_ratio), 3),
        "max_drawdown_pct": round(float(max_drawdown_pct), 2),
        "win_rate_pct": round(float(win_rate_pct), 2),
        "portfolio_value": round(float(equity_curve.iloc[-1]), 2),
    }
