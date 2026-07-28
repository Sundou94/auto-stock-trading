from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

import pandas as pd


@dataclass
class ParamSpec:
    """유전알고리즘이 초기화/변이(mutation) 시 사용하는 파라미터 값의 허용 범위."""

    min: float
    max: float
    is_int: bool = True

    def random_value(self):
        if self.is_int:
            return random.randint(int(self.min), int(self.max))
        return round(random.uniform(self.min, self.max), 4)

    def mutate(self, current: float):
        span = self.max - self.min
        delta = random.uniform(-0.2, 0.2) * span
        value = max(self.min, min(self.max, current + delta))
        return int(round(value)) if self.is_int else round(value, 4)


@dataclass
class StrategyTemplate:
    key: str
    label: str
    description: str
    param_specs: dict[str, ParamSpec]
    signal_fn: Callable[[pd.DataFrame, dict], pd.Series]

    def random_params(self) -> dict:
        return {name: spec.random_value() for name, spec in self.param_specs.items()}

    def mutate_params(self, params: dict) -> dict:
        """파라미터 중 하나만 무작위로 변이시켜 급격한 성격 변화를 방지."""
        mutated = dict(params)
        key = random.choice(list(self.param_specs))
        current = params.get(key, self.param_specs[key].random_value())
        mutated[key] = self.param_specs[key].mutate(current)
        return mutated

    def generate_signals(self, df: pd.DataFrame, params: dict) -> pd.Series:
        return self.signal_fn(df, params)


def positions_from_entry_exit(entry: pd.Series, exit_: pd.Series) -> pd.Series:
    """진입/청산 이벤트 시리즈를 롱-온리 포지션(0=현금, 1=보유) 시리즈로 변환."""
    holding = False
    values = []
    for e, x in zip(entry.fillna(False), exit_.fillna(False)):
        if not holding and e:
            holding = True
        elif holding and x:
            holding = False
        values.append(1 if holding else 0)
    return pd.Series(values, index=entry.index, dtype=int)
