from __future__ import annotations

import numpy as np
import pandas as pd

from app.strategies.base import positions_from_entry_exit


def sma_crossover_signal(df: pd.DataFrame, params: dict) -> pd.Series:
    fast = df["close"].rolling(params["fast_period"]).mean()
    slow = df["close"].rolling(params["slow_period"]).mean()
    return (fast > slow).astype(int)


def rsi_signal(df: pd.DataFrame, params: dict) -> pd.Series:
    period = params["period"]
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    entry = rsi < params["oversold"]
    exit_ = rsi > params["overbought"]
    return positions_from_entry_exit(entry, exit_)


def bollinger_signal(df: pd.DataFrame, params: dict) -> pd.Series:
    period = params["period"]
    mid = df["close"].rolling(period).mean()
    std = df["close"].rolling(period).std()
    upper = mid + params["num_std"] * std
    lower = mid - params["num_std"] * std
    entry = df["close"] < lower
    exit_ = df["close"] > upper
    return positions_from_entry_exit(entry, exit_)


def macd_signal(df: pd.DataFrame, params: dict) -> pd.Series:
    fast_ema = df["close"].ewm(span=params["fast_period"], adjust=False).mean()
    slow_ema = df["close"].ewm(span=params["slow_period"], adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=params["signal_period"], adjust=False).mean()
    return (macd_line > signal_line).astype(int)


def momentum_signal(df: pd.DataFrame, params: dict) -> pd.Series:
    ret = df["close"].pct_change(params["lookback"])
    threshold = params["threshold_pct"] / 100
    return (ret > threshold).astype(int)
