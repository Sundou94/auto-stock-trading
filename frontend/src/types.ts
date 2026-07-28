export interface PerformanceSnapshot {
  id: number;
  trader_id: number;
  total_return_pct: number;
  sharpe_ratio: number;
  max_drawdown_pct: number;
  win_rate_pct: number;
  portfolio_value: number;
  created_at: string;
}

export interface Trader {
  id: number;
  name: string;
  strategy_type: string;
  parameters: Record<string, number>;
  symbol: string;
  generation: number;
  parent_id: number | null;
  is_active: boolean;
  created_at: string;
  retired_at: string | null;
  latest_performance: PerformanceSnapshot | null;
}

export interface Trade {
  id: number;
  side: "buy" | "sell";
  symbol: string;
  qty: number;
  price: number;
  executed_at: string;
}

export interface EvolutionEvent {
  id: number;
  generation: number;
  retired_trader_id: number | null;
  retired_reason: string;
  new_trader_id: number | null;
  method: string;
  created_at: string;
}

export interface StrategyTemplate {
  key: string;
  label: string;
  description: string;
  param_specs: Record<string, { min: number; max: number; is_int: boolean }>;
}
