import { useEffect, useState } from "react";
import { api } from "../api";
import type { StrategyTemplate } from "../types";

export default function Strategies() {
  const [strategies, setStrategies] = useState<StrategyTemplate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .strategies()
      .then(setStrategies)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>불러오는 중...</p>;

  return (
    <div>
      <h1>알고리즘 라이브러리</h1>
      <div className="strategy-grid">
        {strategies.map((s) => (
          <div key={s.key} className="detail-card">
            <h3>{s.label}</h3>
            <p>{s.description}</p>
            <table>
              <thead>
                <tr>
                  <th>파라미터</th>
                  <th>범위</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(s.param_specs).map(([name, spec]) => (
                  <tr key={name}>
                    <td>{name}</td>
                    <td>
                      {spec.min} ~ {spec.max}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}
