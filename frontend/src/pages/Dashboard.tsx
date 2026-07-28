import { useEffect, useState } from "react";
import { api } from "../api";
import TraderCard from "../components/TraderCard";
import type { StrategyTemplate, Trader } from "../types";

export default function Dashboard() {
  const [traders, setTraders] = useState<Trader[]>([]);
  const [strategyMap, setStrategyMap] = useState<Record<string, StrategyTemplate>>({});
  const [account, setAccount] = useState<{ cash: number; portfolio_value: number } | null>(null);
  const [accountError, setAccountError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function loadTraders() {
    setLoading(true);
    try {
      const data = await api.traders();
      data.sort((a, b) => (b.latest_performance?.total_return_pct ?? -Infinity) - (a.latest_performance?.total_return_pct ?? -Infinity));
      setTraders(data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTraders();
    api
      .account()
      .then((a) => setAccount(a))
      .catch((e) => setAccountError(e.message));
    api
      .strategies()
      .then((list) => setStrategyMap(Object.fromEntries(list.map((s) => [s.key, s]))))
      .catch(() => setStrategyMap({}));
  }, []);

  async function handleSeed() {
    setBusy(true);
    setActionMessage(null);
    try {
      await api.seedTraders();
      setActionMessage("10명의 트레이더를 초기 생성했습니다.");
      await loadTraders();
    } catch (e) {
      setActionMessage(`시딩 실패: ${(e as Error).message}`);
    } finally {
      setBusy(false);
    }
  }

  async function handleEvaluate() {
    setBusy(true);
    setActionMessage(null);
    try {
      const result = await api.evaluate();
      setActionMessage(`${result.evaluated}명의 트레이더 성과를 평가했습니다.`);
      await loadTraders();
    } catch (e) {
      setActionMessage(`평가 실패: ${(e as Error).message}`);
    } finally {
      setBusy(false);
    }
  }

  async function handleEvolve() {
    setBusy(true);
    setActionMessage(null);
    try {
      const nextGeneration = Math.max(0, ...traders.map((t) => t.generation)) + 1;
      const events = await api.evolve(nextGeneration);
      setActionMessage(`${events.length}명의 트레이더가 교체되었습니다.`);
      await loadTraders();
    } catch (e) {
      setActionMessage(`진화 실패: ${(e as Error).message}`);
    } finally {
      setBusy(false);
    }
  }

  const activeTraders = traders.filter((t) => t.is_active);

  return (
    <div>
      <section className="summary-bar">
        <div className="summary-card">
          <div className="summary-label">페이퍼 계좌 자산</div>
          <div className="summary-value">
            {account ? `$${account.portfolio_value.toLocaleString()}` : accountError ? "연결 안됨" : "..."}
          </div>
        </div>
        <div className="summary-card">
          <div className="summary-label">활성 트레이더</div>
          <div className="summary-value">{activeTraders.length}명</div>
        </div>
        <div className="summary-card">
          <div className="summary-label">평균 수익률</div>
          <div className="summary-value">
            {activeTraders.length > 0
              ? `${(
                  activeTraders.reduce((sum, t) => sum + (t.latest_performance?.total_return_pct ?? 0), 0) /
                  activeTraders.length
                ).toFixed(2)}%`
              : "-"}
          </div>
        </div>
      </section>

      <section className="action-bar">
        <button onClick={handleSeed} disabled={busy || traders.length > 0}>
          트레이더 10명 시딩
        </button>
        <button onClick={handleEvaluate} disabled={busy || traders.length === 0}>
          성과 평가 실행
        </button>
        <button onClick={handleEvolve} disabled={busy || traders.length === 0}>
          진화 사이클 실행
        </button>
        {actionMessage && <span className="action-message">{actionMessage}</span>}
      </section>

      {loading ? (
        <p>불러오는 중...</p>
      ) : traders.length === 0 ? (
        <p className="empty-state">아직 트레이더가 없습니다. "트레이더 10명 시딩" 버튼으로 시작하세요.</p>
      ) : (
        <div className="trader-grid">
          {traders.map((trader) => (
            <TraderCard key={trader.id} trader={trader} strategyInfo={strategyMap[trader.strategy_type]} />
          ))}
        </div>
      )}
    </div>
  );
}
