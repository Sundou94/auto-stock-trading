import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import type { Trade, Trader } from "../types";

export default function TraderDetail() {
  const { id } = useParams();
  const [trader, setTrader] = useState<Trader | null>(null);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    api
      .trader(Number(id))
      .then(setTrader)
      .catch((e) => setError(e.message));
    api
      .traderTrades(Number(id))
      .then(setTrades)
      .catch(() => setTrades([]));
  }, [id]);

  if (error) return <p className="empty-state">{error}</p>;
  if (!trader) return <p>불러오는 중...</p>;

  const perf = trader.latest_performance;

  return (
    <div>
      <Link to="/" className="back-link">
        ← 대시보드로
      </Link>
      <h1>{trader.name}</h1>
      <p className="trader-detail-subtitle">
        {trader.strategy_type} · {trader.symbol} · 세대 {trader.generation}
        {!trader.is_active && <span className="badge-retired"> 도태됨</span>}
      </p>

      <section className="detail-grid">
        <div className="detail-card">
          <h3>파라미터</h3>
          <table>
            <tbody>
              {Object.entries(trader.parameters).map(([key, value]) => (
                <tr key={key}>
                  <td>{key}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="detail-card">
          <h3>최근 성과</h3>
          {perf ? (
            <table>
              <tbody>
                <tr>
                  <td>총 수익률</td>
                  <td>{perf.total_return_pct.toFixed(2)}%</td>
                </tr>
                <tr>
                  <td>샤프 비율</td>
                  <td>{perf.sharpe_ratio.toFixed(2)}</td>
                </tr>
                <tr>
                  <td>최대 낙폭</td>
                  <td>{perf.max_drawdown_pct.toFixed(2)}%</td>
                </tr>
                <tr>
                  <td>승률</td>
                  <td>{perf.win_rate_pct.toFixed(2)}%</td>
                </tr>
                <tr>
                  <td>평가 포트폴리오 가치</td>
                  <td>${perf.portfolio_value.toLocaleString()}</td>
                </tr>
              </tbody>
            </table>
          ) : (
            <p>아직 평가 기록이 없습니다.</p>
          )}
        </div>
      </section>

      <section className="detail-card">
        <h3>매매 내역</h3>
        {trades.length === 0 ? (
          <p>매매 내역이 없습니다.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>시각</th>
                <th>구분</th>
                <th>종목</th>
                <th>수량</th>
                <th>가격</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade) => (
                <tr key={trade.id}>
                  <td>{new Date(trade.executed_at).toLocaleString()}</td>
                  <td>{trade.side === "buy" ? "매수" : "매도"}</td>
                  <td>{trade.symbol}</td>
                  <td>{trade.qty}</td>
                  <td>${trade.price.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
