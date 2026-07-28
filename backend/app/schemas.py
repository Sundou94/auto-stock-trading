from __future__ import annotations

import datetime

from pydantic import BaseModel, ConfigDict


class TraderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    strategy_type: str
    parameters: dict
    symbol: str
    generation: int
    parent_id: int | None
    is_active: bool
    created_at: datetime.datetime
    retired_at: datetime.datetime | None


class PerformanceSnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    trader_id: int
    total_return_pct: float
    sharpe_ratio: float
    max_drawdown_pct: float
    win_rate_pct: float
    portfolio_value: float
    created_at: datetime.datetime


class TraderDetailOut(TraderOut):
    latest_performance: PerformanceSnapshotOut | None = None


class TradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    side: str
    symbol: str
    qty: float
    price: float
    executed_at: datetime.datetime


class EvolutionEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    generation: int
    retired_trader_id: int | None
    retired_reason: str
    new_trader_id: int | None
    method: str
    created_at: datetime.datetime


class StrategyTemplateOut(BaseModel):
    key: str
    label: str
    description: str
    param_specs: dict
