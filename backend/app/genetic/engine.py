from __future__ import annotations

import random

from sqlalchemy.orm import Session

from app.models import EvolutionEvent, PerformanceSnapshot, Trader, utcnow
from app.strategies.registry import STRATEGY_REGISTRY, random_strategy_type

DEFAULT_SYMBOLS = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"]
POPULATION_SIZE = 10
MIN_RETURN_THRESHOLD_PCT = 0.0  # 이 수익률(%) 미만이면 도태 대상


def seed_initial_population(db: Session, size: int = POPULATION_SIZE) -> list[Trader]:
    traders = []
    for i in range(size):
        strategy_type = random_strategy_type()
        template = STRATEGY_REGISTRY[strategy_type]
        trader = Trader(
            name=f"trader-{i + 1}",
            strategy_type=strategy_type,
            parameters=template.random_params(),
            symbol=random.choice(DEFAULT_SYMBOLS),
            generation=0,
        )
        db.add(trader)
        traders.append(trader)
    db.commit()
    for trader in traders:
        db.refresh(trader)
    return traders


def latest_snapshot(db: Session, trader_id: int) -> PerformanceSnapshot | None:
    return (
        db.query(PerformanceSnapshot)
        .filter(PerformanceSnapshot.trader_id == trader_id)
        .order_by(PerformanceSnapshot.created_at.desc())
        .first()
    )


def _breed(parent_a: Trader, parent_b: Trader | None) -> tuple[str, dict, str]:
    """부모(들)로부터 새 (전략타입, 파라미터)를 생성. 반환값: (strategy_type, params, method)."""
    if parent_b is not None and parent_a.strategy_type == parent_b.strategy_type:
        template = STRATEGY_REGISTRY[parent_a.strategy_type]
        child_params = {
            key: random.choice([parent_a.parameters, parent_b.parameters]).get(key, spec.random_value())
            for key, spec in template.param_specs.items()
        }
        return parent_a.strategy_type, child_params, "crossover"

    # 같은 전략끼리 교배할 짝이 없으면 우수 개체의 파라미터를 변이시켜 재도전
    template = STRATEGY_REGISTRY[parent_a.strategy_type]
    return parent_a.strategy_type, template.mutate_params(parent_a.parameters), "mutation"


def evolve_generation(
    db: Session,
    generation: int,
    min_return_threshold_pct: float = MIN_RETURN_THRESHOLD_PCT,
) -> list[EvolutionEvent]:
    """평가 주기마다 호출: 기준 수익률 미달 트레이더를 도태시키고 우수 개체 교배/변이로 대체한다."""
    active = db.query(Trader).filter(Trader.is_active.is_(True)).all()
    scored = [(t, latest_snapshot(db, t.id)) for t in active]
    scored = [(t, s) for t, s in scored if s is not None]
    if not scored:
        return []

    scored.sort(key=lambda pair: pair[1].total_return_pct, reverse=True)
    top_performers = [t for t, _ in scored[: max(2, len(scored) // 2)]]
    underperformers = [(t, s) for t, s in scored if s.total_return_pct < min_return_threshold_pct]

    events: list[EvolutionEvent] = []
    for trader, snapshot in underperformers:
        trader.is_active = False
        trader.retired_at = utcnow()
        db.add(trader)

        parent_a = random.choice(top_performers)
        parent_b = random.choice(top_performers) if len(top_performers) > 1 else None
        strategy_type, params, method = _breed(parent_a, parent_b)

        child = Trader(
            name=f"trader-{trader.id}-gen{generation}",
            strategy_type=strategy_type,
            parameters=params,
            symbol=trader.symbol,
            generation=generation,
            parent_id=parent_a.id,
        )
        db.add(child)
        db.flush()

        event = EvolutionEvent(
            generation=generation,
            retired_trader_id=trader.id,
            retired_reason=f"수익률 {snapshot.total_return_pct}% (기준 {min_return_threshold_pct}% 미달)",
            new_trader_id=child.id,
            method=method,
        )
        db.add(event)
        events.append(event)

    db.commit()
    return events
