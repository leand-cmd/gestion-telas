import { colors } from "../../theme/colors";

interface GestionesBarListProps {
  data: { tipo: string; cantidad: number }[];
}

export function GestionesBarList({ data }: GestionesBarListProps) {
  if (data.length === 0) {
    return (
      <p style={{ fontSize: 13, color: colors.grayNeutral, margin: 0 }}>
        Sin gestiones registradas este mes.
      </p>
    );
  }

  const max = Math.max(...data.map((d) => d.cantidad));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      {data.map((d) => (
        <div key={d.tipo}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: 12,
              marginBottom: 4,
              gap: 8,
            }}
          >
            <span style={{ color: "#4a4a5a" }}>{d.tipo}</span>
            <span style={{ fontWeight: 700, color: colors.purpleDark, flexShrink: 0 }}>
              {d.cantidad}
            </span>
          </div>
          <div style={{ height: 8, borderRadius: 4, background: colors.grayLight }}>
            <div
              style={{
                height: "100%",
                borderRadius: 4,
                width: `${(d.cantidad / max) * 100}%`,
                background: colors.purplePrimary,
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
