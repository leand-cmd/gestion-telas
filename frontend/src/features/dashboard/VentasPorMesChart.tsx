import { useState } from "react";

import { colors } from "../../theme/colors";

interface VentasPorMesChartProps {
  data: { mes: string; total: number }[];
}

function formatMes(mes: string) {
  const [year, month] = mes.split("-").map(Number);
  const fecha = new Date(year, month - 1, 1);
  return fecha.toLocaleDateString("es-PY", { month: "short" });
}

export function VentasPorMesChart({ data }: VentasPorMesChartProps) {
  const [hovered, setHovered] = useState<number | null>(null);
  const max = Math.max(1, ...data.map((d) => d.total));
  const peakIndex = data.reduce(
    (best, d, i) => (d.total > (data[best]?.total ?? -1) ? i : best),
    0
  );

  return (
    <div className="table-scroll">
      <div style={{ minWidth: 360 }}>
      <div
        style={{
          display: "flex",
          alignItems: "flex-end",
          gap: 16,
          height: 180,
          borderBottom: `1px solid ${colors.grayLight}`,
          padding: "24px 8px 0",
        }}
      >
        {data.map((d, i) => {
          const alturaPx = Math.max(4, (d.total / max) * 150);
          const activo = hovered === i;
          return (
            <div
              key={d.mes}
              style={{
                flex: 1,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                position: "relative",
              }}
              onMouseEnter={() => setHovered(i)}
              onMouseLeave={() => setHovered(null)}
            >
              {(activo || i === peakIndex) && (
                <div
                  style={{
                    position: "absolute",
                    bottom: alturaPx + 6,
                    fontSize: 11,
                    fontWeight: 700,
                    color: colors.purpleDark,
                    whiteSpace: "nowrap",
                  }}
                >
                  ₲ {d.total.toLocaleString("es-PY")}
                </div>
              )}
              <div
                style={{
                  width: "100%",
                  maxWidth: 40,
                  height: alturaPx,
                  borderRadius: "4px 4px 0 0",
                  background: activo ? colors.purpleDark : colors.purplePrimary,
                  transition: "background 0.15s",
                }}
              />
            </div>
          );
        })}
      </div>
      <div style={{ display: "flex", gap: 16, padding: "8px 8px 0" }}>
        {data.map((d) => (
          <div
            key={d.mes}
            style={{ flex: 1, textAlign: "center", fontSize: 12, color: colors.grayNeutral }}
          >
            {formatMes(d.mes)}
          </div>
        ))}
      </div>
      </div>
    </div>
  );
}
