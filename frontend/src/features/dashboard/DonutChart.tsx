import { colors } from "../../theme/colors";

interface DonutChartProps {
  percentage: number;
  color?: string;
  label?: string;
}

export function DonutChart({ percentage, color = colors.purplePrimary, label }: DonutChartProps) {
  const pct = Math.max(0, Math.min(100, percentage));

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
      <div
        style={{
          width: 140,
          height: 140,
          borderRadius: "50%",
          background: `conic-gradient(${color} ${pct * 3.6}deg, ${colors.grayLight} 0deg)`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
        }}
      >
        <div
          style={{
            width: 100,
            height: 100,
            borderRadius: "50%",
            background: colors.white,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <span style={{ fontSize: 22, fontWeight: 800, color: colors.purpleDark }}>
            {pct.toLocaleString("es-PY", { maximumFractionDigits: 1 })}%
          </span>
        </div>
      </div>
      {label && (
        <span style={{ fontSize: 12, color: colors.grayNeutral, textAlign: "center" }}>{label}</span>
      )}
    </div>
  );
}
