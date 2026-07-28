import { Link } from "react-router-dom";
import type { StrategyTemplate, Trader } from "../types";
import PixelTrader from "./PixelTrader";

const STRATEGY_LABELS: Record<string, string> = {
  sma_crossover: "이동평균 교차",
  rsi: "RSI",
  bollinger: "볼린저 밴드",
  macd: "MACD",
  momentum: "모멘텀",
};

function formatPct(value: number | undefined) {
  if (value === undefined) return "-";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

export default function TraderCard({
  trader,
  strategyInfo,
}: {
  trader: Trader;
  strategyInfo?: StrategyTemplate;
}) {
  const perf = trader.latest_performance;
  const returnClass = perf ? (perf.total_return_pct >= 0 ? "positive" : "negative") : "";

  return (
    <Link to={`/traders/${trader.id}`} className={`trader-card ${trader.is_active ? "" : "retired"}`}>
      <PixelTrader trader={trader} strategyInfo={strategyInfo} />
      <div className="trader-card-header">
        <span className="trader-name">{trader.name}</span>
        <span className="trader-strategy">{STRATEGY_LABELS[trader.strategy_type] ?? trader.strategy_type}</span>
      </div>
      <div className="trader-symbol">{trader.symbol}</div>
      <div className={`trader-return ${returnClass}`}>{formatPct(perf?.total_return_pct)}</div>
      <div className="trader-metrics">
        <span>샤프 {perf ? perf.sharpe_ratio.toFixed(2) : "-"}</span>
        <span>MDD {perf ? `${perf.max_drawdown_pct.toFixed(1)}%` : "-"}</span>
        <span>승률 {perf ? `${perf.win_rate_pct.toFixed(0)}%` : "-"}</span>
      </div>
      <div className="trader-footer">
        <span>세대 {trader.generation}</span>
        {!trader.is_active && <span className="badge-retired">도태됨</span>}
      </div>
    </Link>
  );
}
