import type { EvolutionEvent, StrategyTemplate, Trade, Trader } from "./types";

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${detail}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string }>("/health"),
  account: () =>
    request<{ status: string; cash: number; portfolio_value: number; buying_power: number }>("/account"),
  strategies: () => request<StrategyTemplate[]>("/strategies"),
  traders: (activeOnly = false) => request<Trader[]>(`/traders?active_only=${activeOnly}`),
  trader: (id: number) => request<Trader>(`/traders/${id}`),
  traderTrades: (id: number) => request<Trade[]>(`/traders/${id}/trades`),
  seedTraders: () => request<Trader[]>("/traders/seed", { method: "POST" }),
  evaluate: () => request<{ evaluated: number }>("/evaluate", { method: "POST" }),
  evolve: (generation: number, minReturnThresholdPct = 0) =>
    request<EvolutionEvent[]>(
      `/evolve?generation=${generation}&min_return_threshold_pct=${minReturnThresholdPct}`,
      { method: "POST" },
    ),
  evolutionHistory: () => request<EvolutionEvent[]>("/evolution"),
};
