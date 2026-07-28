from __future__ import annotations

import datetime as dt

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest

from app.config import settings


def _trading_client() -> TradingClient:
    return TradingClient(settings.alpaca_api_key_id, settings.alpaca_api_secret_key, paper=True)


def _data_client() -> StockHistoricalDataClient:
    return StockHistoricalDataClient(settings.alpaca_api_key_id, settings.alpaca_api_secret_key)


def get_account() -> dict:
    account = _trading_client().get_account()
    return {
        "status": account.status,
        "cash": float(account.cash),
        "portfolio_value": float(account.portfolio_value),
        "buying_power": float(account.buying_power),
    }


def get_daily_bars(symbol: str, lookback_days: int = 400) -> pd.DataFrame:
    client = _data_client()
    end = dt.datetime.now(dt.timezone.utc)
    start = end - dt.timedelta(days=lookback_days)
    request = StockBarsRequest(symbol_or_symbols=symbol, timeframe=TimeFrame.Day, start=start, end=end)
    bars = client.get_stock_bars(request).df
    if isinstance(bars.index, pd.MultiIndex):
        bars = bars.xs(symbol, level=0)
    return bars[["open", "high", "low", "close", "volume"]]


def submit_paper_order(symbol: str, qty: float, side: str):
    client = _trading_client()
    order = MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    return client.submit_order(order)
