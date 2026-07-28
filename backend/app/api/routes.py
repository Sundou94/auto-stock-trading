from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.alpaca_client import get_account
from app.database import get_db
from app.evaluation import evaluate_all_traders
from app.genetic.engine import evolve_generation, latest_snapshot, seed_initial_population
from app.models import EvolutionEvent, Trade, Trader
from app.schemas import (
    EvolutionEventOut,
    StrategyTemplateOut,
    TradeOut,
    TraderDetailOut,
    TraderOut,
)
from app.strategies.registry import STRATEGY_REGISTRY

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/account")
def account():
    try:
        return get_account()
    except Exception as exc:  # Alpaca 키 미설정/오류
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/strategies", response_model=list[StrategyTemplateOut])
def list_strategies():
    return [
        StrategyTemplateOut(
            key=t.key,
            label=t.label,
            description=t.description,
            param_specs={
                name: {"min": s.min, "max": s.max, "is_int": s.is_int} for name, s in t.param_specs.items()
            },
        )
        for t in STRATEGY_REGISTRY.values()
    ]


@router.post("/traders/seed", response_model=list[TraderOut])
def seed_traders(db: Session = Depends(get_db)):
    if db.query(Trader).count() > 0:
        raise HTTPException(status_code=400, detail="이미 트레이더가 존재합니다.")
    return seed_initial_population(db)


@router.get("/traders", response_model=list[TraderDetailOut])
def list_traders(active_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Trader)
    if active_only:
        query = query.filter(Trader.is_active.is_(True))
    traders = query.order_by(Trader.id).all()

    results = []
    for trader in traders:
        item = TraderDetailOut.model_validate(trader)
        item.latest_performance = latest_snapshot(db, trader.id)
        results.append(item)
    return results


@router.get("/traders/{trader_id}", response_model=TraderDetailOut)
def get_trader(trader_id: int, db: Session = Depends(get_db)):
    trader = db.get(Trader, trader_id)
    if trader is None:
        raise HTTPException(status_code=404, detail="트레이더를 찾을 수 없습니다.")
    item = TraderDetailOut.model_validate(trader)
    item.latest_performance = latest_snapshot(db, trader.id)
    return item


@router.get("/traders/{trader_id}/trades", response_model=list[TradeOut])
def get_trader_trades(trader_id: int, db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.trader_id == trader_id).order_by(Trade.executed_at.desc()).all()


@router.post("/evaluate")
def evaluate(db: Session = Depends(get_db)):
    snapshots = evaluate_all_traders(db)
    return {"evaluated": len(snapshots)}


@router.post("/evolve", response_model=list[EvolutionEventOut])
def evolve(generation: int, min_return_threshold_pct: float = 0.0, db: Session = Depends(get_db)):
    return evolve_generation(db, generation=generation, min_return_threshold_pct=min_return_threshold_pct)


@router.get("/evolution", response_model=list[EvolutionEventOut])
def evolution_history(db: Session = Depends(get_db)):
    return db.query(EvolutionEvent).order_by(EvolutionEvent.created_at.desc()).all()
