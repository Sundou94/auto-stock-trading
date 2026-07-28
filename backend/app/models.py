import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class Trader(Base):
    """유전알고리즘의 개체(population member) 하나 = 트레이더 한 명."""

    __tablename__ = "traders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="")
    strategy_type: Mapped[str] = mapped_column(String)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    symbol: Mapped[str] = mapped_column(String, default="AAPL")

    generation: Mapped[int] = mapped_column(Integer, default=0)
    parent_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    cash: Mapped[float] = mapped_column(Float, default=10000.0)
    position_qty: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utcnow)
    retired_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

    trades: Mapped[list["Trade"]] = relationship(back_populates="trader", cascade="all, delete-orphan")
    snapshots: Mapped[list["PerformanceSnapshot"]] = relationship(
        back_populates="trader", cascade="all, delete-orphan"
    )


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trader_id: Mapped[int] = mapped_column(ForeignKey("traders.id"))
    side: Mapped[str] = mapped_column(String)  # buy | sell
    symbol: Mapped[str] = mapped_column(String)
    qty: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    executed_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utcnow)

    trader: Mapped["Trader"] = relationship(back_populates="trades")


class PerformanceSnapshot(Base):
    """평가 주기마다 계산되는 트레이더 성과 스냅샷 (유전알고리즘의 fitness 근거)."""

    __tablename__ = "performance_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trader_id: Mapped[int] = mapped_column(ForeignKey("traders.id"))
    total_return_pct: Mapped[float] = mapped_column(Float, default=0.0)
    sharpe_ratio: Mapped[float] = mapped_column(Float, default=0.0)
    max_drawdown_pct: Mapped[float] = mapped_column(Float, default=0.0)
    win_rate_pct: Mapped[float] = mapped_column(Float, default=0.0)
    portfolio_value: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utcnow)

    trader: Mapped["Trader"] = relationship(back_populates="snapshots")


class EvolutionEvent(Base):
    """세대 교체 로그: 어떤 트레이더가 왜 도태되고 무엇으로 대체됐는지."""

    __tablename__ = "evolution_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    generation: Mapped[int] = mapped_column(Integer)
    retired_trader_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    retired_reason: Mapped[str] = mapped_column(String, default="")
    new_trader_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    method: Mapped[str] = mapped_column(String, default="")  # crossover | mutation | fresh_seed
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utcnow)
