import { colors } from "../../theme/colors";
import { colorForTipoGestion } from "./gestionColors";

interface GestionesPieChartProps {
  data: { tipo: string; cantidad: number }[];
}

export function GestionesPieChart({ data }: GestionesPieChartProps) {
  const total = data.reduce((acc, d) => acc + d.cantidad, 0);

  if (total === 0) {
    return (
      <p style={{ fontSize: 13, color: colors.grayNeutral, margin: 0 }}>
        Sin gestiones registradas este mes.
      </p>
    );
  }

  let acumulado = 0;
  const stops = data.map((d) => {
    const desde = (acumulado / total) * 360;
    acumulado += d.cantidad;
    const hasta = (acumulado / total) * 360;
    return `${colorForTipoGestion(d.tipo)} ${desde}deg ${hasta}deg`;
  });

  return (
    <div style={{ display: "flex", gap: 20, alignItems: "center", flexWrap: "wrap" }}>
      <div
        style={{
          width: 140,
          height: 140,
          borderRadius: "50%",
          background: `conic-gradient(${stops.join(", ")})`,
          flexShrink: 0,
        }}
      />
      <div style={{ display: "flex", flexDirection: "column", gap: 6, flex: 1, minWidth: 160 }}>
        {data.map((d) => (
          <div key={d.tipo} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 12 }}>
            <span
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                background: colorForTipoGestion(d.tipo),
                flexShrink: 0,
              }}
            />
            <span style={{ color: "#4a4a5a", flex: 1 }}>{d.tipo}</span>
            <span style={{ fontWeight: 700, color: colors.purpleDark }}>
              {Math.round((d.cantidad / total) * 100)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
