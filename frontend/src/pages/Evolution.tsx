import { useEffect, useState } from "react";
import { api } from "../api";
import type { EvolutionEvent } from "../types";

const METHOD_LABELS: Record<string, string> = {
  crossover: "교차",
  mutation: "변이",
  fresh_seed: "신규 시딩",
};

export default function Evolution() {
  const [events, setEvents] = useState<EvolutionEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .evolutionHistory()
      .then(setEvents)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>불러오는 중...</p>;
  if (events.length === 0) return <p className="empty-state">아직 진화 이벤트가 없습니다.</p>;

  return (
    <div>
      <h1>진화 히스토리</h1>
      <ul className="timeline">
        {events.map((event) => (
          <li key={event.id} className="timeline-item">
            <div className="timeline-generation">세대 {event.generation}</div>
            <div className="timeline-body">
              <div>
                트레이더 #{event.retired_trader_id} 도태 → #{event.new_trader_id} 로 대체 (
                {METHOD_LABELS[event.method] ?? event.method})
              </div>
              <div className="timeline-reason">{event.retired_reason}</div>
              <div className="timeline-time">{new Date(event.created_at).toLocaleString()}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
