import { useMemo, useState } from "react";
import type { StrategyTemplate, Trader } from "../types";

const PIXEL_SIZE = 3;

// 8(가로) x 11(세로) 도트 캐릭터. O=외곽선, H/A=피부, E=눈, B=몸통(전략별 색상)
const GRID = [
  "...OO...",
  "..OHHO..",
  ".OEHHEO.",
  ".OHHHHO.",
  "...OO...",
  "..OBBO..",
  ".ABBBBA.",
  ".OBBBBO.",
  "..OBBO..",
  "..O..O..",
  "..O..O..",
];

const STRATEGY_COLORS: Record<string, string> = {
  sma_crossover: "#4f8cff",
  rsi: "#ffb84f",
  bollinger: "#a374ff",
  macd: "#34d399",
  momentum: "#f472b6",
};

const FALLBACK_LABELS: Record<string, string> = {
  sma_crossover: "이동평균 교차",
  rsi: "RSI",
  bollinger: "볼린저 밴드",
  macd: "MACD",
  momentum: "모멘텀",
};

function buildBoxShadow(bodyColor: string): string {
  const baseColors: Record<string, string> = {
    O: "#14142b",
    H: "#f4c99b",
    A: "#f4c99b",
    E: "#ffffff",
    B: bodyColor,
  };
  const shadows: string[] = [];
  GRID.forEach((row, y) => {
    [...row].forEach((cell, x) => {
      if (cell === ".") return;
      shadows.push(`${x * PIXEL_SIZE}px ${y * PIXEL_SIZE}px 0 ${baseColors[cell]}`);
    });
  });
  return shadows.join(", ");
}

export default function PixelTrader({
  trader,
  strategyInfo,
}: {
  trader: Trader;
  strategyInfo?: StrategyTemplate;
}) {
  const [showInfo, setShowInfo] = useState(false);
  const bodyColor = STRATEGY_COLORS[trader.strategy_type] ?? "#94a3b8";
  const boxShadow = useMemo(() => buildBoxShadow(bodyColor), [bodyColor]);

  const returnPct = trader.latest_performance?.total_return_pct;
  const chipColor = returnPct === undefined ? "#94a3b8" : returnPct >= 0 ? "#22c55e" : "#ef4444";
  const bobDelay = `${(trader.id % 5) * 0.15}s`;
  const chipDelay = `${(trader.id % 3) * 0.2}s`;

  const label = strategyInfo?.label ?? FALLBACK_LABELS[trader.strategy_type] ?? trader.strategy_type;
  const description = strategyInfo?.description ?? "";

  function handleClick(e: React.MouseEvent) {
    e.preventDefault();
    e.stopPropagation();
    setShowInfo((v) => !v);
  }

  return (
    <div className="pixel-trader-wrap">
      <button
        type="button"
        className="pixel-trader-avatar"
        style={{ animationDelay: bobDelay }}
        onClick={handleClick}
        aria-label={`${trader.name} 알고리즘 설명 보기`}
      >
        <span className="pixel-body" style={{ boxShadow, animationDelay: bobDelay }} />
        <span
          className="pixel-chip"
          style={{ backgroundColor: chipColor, animationDelay: chipDelay }}
        />
      </button>

      {showInfo && (
        <div className="pixel-popover" onClick={(e) => e.stopPropagation()}>
          <div className="pixel-popover-title">{label}</div>
          <p className="pixel-popover-desc">{description || "설명을 불러오지 못했습니다."}</p>
          <div className="pixel-popover-params">
            {Object.entries(trader.parameters).map(([key, value]) => (
              <span key={key} className="param-chip">
                {key}={value}
              </span>
            ))}
          </div>
          <button type="button" className="pixel-popover-close" onClick={handleClick}>
            닫기
          </button>
        </div>
      )}
    </div>
  );
}
