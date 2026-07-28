import random

from app.strategies import templates as t
from app.strategies.base import ParamSpec, StrategyTemplate

STRATEGY_REGISTRY: dict[str, StrategyTemplate] = {
    "sma_crossover": StrategyTemplate(
        key="sma_crossover",
        label="이동평균 교차",
        description="단기 이동평균이 장기 이동평균을 상향 돌파하면 매수 상태 유지, 하향 돌파하면 매도",
        param_specs={
            "fast_period": ParamSpec(5, 20),
            "slow_period": ParamSpec(20, 60),
        },
        signal_fn=t.sma_crossover_signal,
    ),
    "rsi": StrategyTemplate(
        key="rsi",
        label="RSI 과매수/과매도",
        description="RSI가 과매도 구간에 진입하면 매수, 과매수 구간에 진입하면 매도",
        param_specs={
            "period": ParamSpec(7, 21),
            "oversold": ParamSpec(20, 35),
            "overbought": ParamSpec(65, 80),
        },
        signal_fn=t.rsi_signal,
    ),
    "bollinger": StrategyTemplate(
        key="bollinger",
        label="볼린저 밴드",
        description="가격이 하단 밴드 아래로 내려가면 매수, 상단 밴드 위로 올라가면 매도",
        param_specs={
            "period": ParamSpec(10, 30),
            "num_std": ParamSpec(1.5, 3.0, is_int=False),
        },
        signal_fn=t.bollinger_signal,
    ),
    "macd": StrategyTemplate(
        key="macd",
        label="MACD",
        description="MACD 라인이 시그널 라인 위에 있는 동안 매수 상태 유지",
        param_specs={
            "fast_period": ParamSpec(8, 15),
            "slow_period": ParamSpec(20, 30),
            "signal_period": ParamSpec(5, 12),
        },
        signal_fn=t.macd_signal,
    ),
    "momentum": StrategyTemplate(
        key="momentum",
        label="모멘텀",
        description="일정 기간 수익률이 임계값을 넘으면 매수 상태 유지",
        param_specs={
            "lookback": ParamSpec(5, 30),
            "threshold_pct": ParamSpec(0, 5, is_int=False),
        },
        signal_fn=t.momentum_signal,
    ),
}


def random_strategy_type() -> str:
    return random.choice(list(STRATEGY_REGISTRY))
