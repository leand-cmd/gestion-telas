import { useMemo, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { fetchClientes } from "../clientes/clientesApi";
import { addDays, NOMBRES_MES, startOfWeekMonday, toISODate } from "./calendarUtils";
import { ReagendarVisitaForm } from "./ReagendarVisitaForm";
import { VisitaDetalleModal } from "./VisitaDetalleModal";
import { VisitaForm } from "./VisitaForm";
import { VisitaResultadoForm } from "./VisitaResultadoForm";
import { VisitasCalendar } from "./VisitasCalendar";
import { ESTADO_COLORS, ESTADO_LABELS } from "./visitaEstadoColors";
import { fetchVisitas } from "./visitasApi";

type ViewMode = "mes" | "semana";

export function VisitasList() {
  const [anchorDate, setAnchorDate] = useState(new Date());
  const [viewMode, setViewMode] = useState<ViewMode>("mes");
  const [clienteFiltro, setClienteFiltro] = useState<number | "">("");
  const [selectedDate, setSelectedDate] = useState<Date | null>(new Date());
  const [formOpen, setFormOpen] = useState(false);
  const [detalleVisita, setDetalleVisita] = useState<Visita | null>(null);
  const [registrandoResultado, setRegistrandoResultado] = useState<Visita | null>(null);
  const [reagendando, setReagendando] = useState<Visita | null>(null);

  const queryClient = useQueryClient();

  const { desde, hasta } = useMemo(() => {
    if (viewMode === "semana") {
      const inicio = startOfWeekMonday(anchorDate);
      return { desde: toISODate(inicio), hasta: toISODate(addDays(inicio, 6)) };
    }
    const primerDiaMes = new Date(anchorDate.getFullYear(), anchorDate.getMonth(), 1);
    const inicio = startOfWeekMonday(primerDiaMes);
    return { desde: toISODate(inicio), hasta: toISODate(addDays(inicio, 41)) };
  }, [anchorDate, viewMode]);

  const { data: clientesData } = useQuery({
    queryKey: ["clientes-select"],
    queryFn: () => fetchClientes({ page: 1, per_page: 200 }),
  });

  const { data, isLoading } = useQuery({
    queryKey: ["visitas", { desde, hasta, clienteFiltro }],
    queryFn: () =>
      fetchVisitas({
        desde,
        hasta,
        cliente_id: clienteFiltro || undefined,
        per_page: 200,
      }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["visitas"] });

  const visitas = data?.items ?? [];
  const visitasDelDia = selectedDate
    ? visitas
        .filter((v) => v.fecha === toISODate(selectedDate))
        .slice()
        .sort((a, b) => a.hora.localeCompare(b.hora))
    : [];

  const cambiarPeriodo = (direccion: 1 | -1) => {
    if (viewMode === "semana") {
      setAnchorDate((d) => addDays(d, 7 * direccion));
    } else {
      setAnchorDate((d) => new Date(d.getFullYear(), d.getMonth() + direccion, 1));
    }
  };

  const irAHoy = () => {
    const hoy = new Date();
    setAnchorDate(hoy);
    setSelectedDate(hoy);
  };

  const tituloPeriodo =
    viewMode === "mes"
      ? `${NOMBRES_MES[anchorDate.getMonth()]} ${anchorDate.getFullYear()}`
      : (() => {
          const inicio = startOfWeekMonday(anchorDate);
          const fin = addDays(inicio, 6);
          return `${inicio.getDate()}/${inicio.getMonth() + 1} — ${fin.getDate()}/${fin.getMonth() + 1}`;
        })();

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Visitas y Agenda</h2>
        <button className="btn btn-primary" onClick={() => setFormOpen(true)}>
          + Programar Visita
        </button>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <button className="btn btn-secondary" onClick={() => cambiarPeriodo(-1)}>
            ‹
          </button>
          <span style={{ fontWeight: 700, color: colors.purpleDark, minWidth: 140, textAlign: "center" }}>
            {tituloPeriodo}
          </span>
          <button className="btn btn-secondary" onClick={() => cambiarPeriodo(1)}>
            ›
          </button>
          <button className="btn btn-secondary" onClick={irAHoy}>
            Hoy
          </button>
        </div>

        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <select value={viewMode} onChange={(e) => setViewMode(e.target.value as ViewMode)}>
            <option value="mes">Mes</option>
            <option value="semana">Semana</option>
          </select>
          <select
            value={clienteFiltro}
            onChange={(e) => setClienteFiltro(e.target.value ? Number(e.target.value) : "")}
          >
            <option value="">Todos los clientes</option>
            {(clientesData?.items ?? []).map((c) => (
              <option key={c.id} value={c.id}>
                {c.razon_social}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="split-layout">
        <div className="card">
          {isLoading ? (
            <div style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>Cargando...</div>
          ) : (
            <VisitasCalendar
              anchorDate={anchorDate}
              viewMode={viewMode}
              visitas={visitas}
              selectedDate={selectedDate}
              onSelectDate={setSelectedDate}
              onSelectVisita={setDetalleVisita}
            />
          )}
        </div>

        <div className="card">
          <h3 style={{ margin: "0 0 12px", color: colors.purpleDark, fontSize: 15 }}>
            {selectedDate
              ? `Visitas del ${selectedDate.getDate()}/${selectedDate.getMonth() + 1}`
              : "Seleccioná un día"}
          </h3>
          {visitasDelDia.length === 0 ? (
            <p style={{ fontSize: 13, color: colors.grayNeutral, margin: 0 }}>
              No hay visitas programadas para este día.
            </p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {visitasDelDia.map((v) => {
                const c = ESTADO_COLORS[v.estado];
                return (
                  <div
                    key={v.id}
                    style={{
                      padding: 10,
                      borderRadius: 12,
                      background: colors.grayLight,
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      gap: 8,
                    }}
                  >
                    <div style={{ minWidth: 0 }}>
                      <div style={{ fontWeight: 700, fontSize: 13, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                        {v.hora} — {v.cliente?.razon_social ?? "-"}
                      </div>
                      <div style={{ fontSize: 12, color: colors.grayNeutral }}>{v.proposito ?? "-"}</div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
                      <span className="badge" style={{ background: c.bg, color: c.text }}>
                        {ESTADO_LABELS[v.estado]}
                      </span>
                      <button className="btn btn-secondary" onClick={() => setDetalleVisita(v)}>
                        Ver detalle
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {formOpen && (
        <VisitaForm
          onClose={() => setFormOpen(false)}
          onSaved={() => {
            setFormOpen(false);
            refetch();
          }}
        />
      )}

      {detalleVisita && (
        <VisitaDetalleModal
          visita={detalleVisita}
          onClose={() => setDetalleVisita(null)}
          onChanged={refetch}
          onRegistrarResultado={(v) => {
            setDetalleVisita(null);
            setRegistrandoResultado(v);
          }}
          onReagendar={(v) => {
            setDetalleVisita(null);
            setReagendando(v);
          }}
        />
      )}

      {registrandoResultado && (
        <VisitaResultadoForm
          visita={registrandoResultado}
          onClose={() => setRegistrandoResultado(null)}
          onSaved={() => {
            setRegistrandoResultado(null);
            refetch();
          }}
        />
      )}

      {reagendando && (
        <ReagendarVisitaForm
          visita={reagendando}
          onClose={() => setReagendando(null)}
          onSaved={() => {
            setReagendando(null);
            refetch();
          }}
        />
      )}
    </div>
  );
}
