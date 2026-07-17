import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { addDays, DIAS_SEMANA, isSameDay, startOfWeekMonday, toISODate } from "./calendarUtils";
import { colorParaEstadoVisita } from "./visitaEstadoColors";

interface VisitasCalendarProps {
  anchorDate: Date;
  viewMode: "mes" | "semana";
  visitas: Visita[];
  selectedDate: Date | null;
  onSelectDate: (date: Date) => void;
  onSelectVisita: (visita: Visita) => void;
}

export function VisitasCalendar({
  anchorDate,
  viewMode,
  visitas,
  selectedDate,
  onSelectDate,
  onSelectVisita,
}: VisitasCalendarProps) {
  const hoy = new Date();

  const visitasPorDia = new Map<string, Visita[]>();
  for (const v of visitas) {
    const lista = visitasPorDia.get(v.fecha) ?? [];
    lista.push(v);
    visitasPorDia.set(v.fecha, lista);
  }

  let cells: Date[];
  if (viewMode === "semana") {
    const inicio = startOfWeekMonday(anchorDate);
    cells = Array.from({ length: 7 }, (_, i) => addDays(inicio, i));
  } else {
    const primerDiaMes = new Date(anchorDate.getFullYear(), anchorDate.getMonth(), 1);
    const inicio = startOfWeekMonday(primerDiaMes);
    cells = Array.from({ length: 42 }, (_, i) => addDays(inicio, i));
  }

  const maxChips = viewMode === "semana" ? 6 : 3;

  return (
    <div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, 1fr)",
          gap: 4,
          marginBottom: 4,
        }}
      >
        {DIAS_SEMANA.map((d) => (
          <div
            key={d}
            style={{
              textAlign: "center",
              fontSize: 12,
              fontWeight: 700,
              color: colors.grayNeutral,
              padding: "4px 0",
            }}
          >
            {d}
          </div>
        ))}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, 1fr)",
          gap: 4,
        }}
      >
        {cells.map((date) => {
          const iso = toISODate(date);
          const esMesActual = viewMode === "semana" || date.getMonth() === anchorDate.getMonth();
          const esHoy = isSameDay(date, hoy);
          const esSeleccionado = selectedDate != null && isSameDay(date, selectedDate);
          const visitasDia = (visitasPorDia.get(iso) ?? []).slice().sort((a, b) => a.hora.localeCompare(b.hora));
          const visibles = visitasDia.slice(0, maxChips);
          const restantes = visitasDia.length - visibles.length;

          return (
            <div
              key={iso}
              onClick={() => onSelectDate(date)}
              style={{
                minHeight: viewMode === "semana" ? 220 : 90,
                borderRadius: 12,
                border: esSeleccionado
                  ? `2px solid ${colors.purplePrimary}`
                  : "1px solid " + colors.grayLight,
                background: esMesActual ? colors.white : colors.grayLight,
                opacity: esMesActual ? 1 : 0.6,
                padding: 6,
                cursor: "pointer",
                display: "flex",
                flexDirection: "column",
                gap: 4,
              }}
            >
              <div
                style={{
                  fontSize: 12,
                  fontWeight: esHoy ? 800 : 600,
                  color: esHoy ? colors.purpleDark : "#4a4a5a",
                  display: "flex",
                  alignItems: "center",
                  gap: 4,
                }}
              >
                {esHoy && (
                  <span
                    style={{
                      width: 6,
                      height: 6,
                      borderRadius: "50%",
                      background: colors.purplePrimary,
                    }}
                  />
                )}
                {date.getDate()}
              </div>

              {visibles.map((v) => {
                const c = colorParaEstadoVisita(v.estado);
                return (
                  <div
                    key={v.id}
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectVisita(v);
                    }}
                    style={{
                      fontSize: 11,
                      background: c.bg,
                      color: c.text,
                      borderRadius: 6,
                      padding: "2px 6px",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                      fontWeight: 600,
                    }}
                    title={`${v.hora} — ${v.cliente?.razon_social ?? ""}`}
                  >
                    {v.hora} {v.cliente?.razon_social ?? ""}
                  </div>
                );
              })}
              {restantes > 0 && (
                <div style={{ fontSize: 11, color: colors.grayNeutral, fontWeight: 600 }}>
                  +{restantes} más
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
