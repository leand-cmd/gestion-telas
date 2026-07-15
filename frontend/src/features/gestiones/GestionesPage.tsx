import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { fetchClientes } from "../clientes/clientesApi";
import { fetchResumen } from "../dashboard/dashboardApi";
import { DonutChart } from "../dashboard/DonutChart";
import { GestionesBarList } from "../dashboard/GestionesBarList";
import { VisitaResultadoForm } from "../visitas/VisitaResultadoForm";
import { TIPOS_GESTION } from "../visitas/visitaOptions";
import { deleteVisita, fetchVisitas } from "../visitas/visitasApi";
import { GestionesPieChart } from "./GestionesPieChart";

export function GestionesPage() {
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [tipoGestion, setTipoGestion] = useState("");
  const [clienteFiltro, setClienteFiltro] = useState<number | "">("");
  const [editando, setEditando] = useState<Visita | null>(null);
  const [eliminando, setEliminando] = useState<Visita | null>(null);

  const queryClient = useQueryClient();

  const { data: clientesData } = useQuery({
    queryKey: ["clientes-select"],
    queryFn: () => fetchClientes({ page: 1, per_page: 200 }),
  });

  const { data: resumen } = useQuery({ queryKey: ["dashboard"], queryFn: fetchResumen });

  const { data, isLoading } = useQuery({
    queryKey: ["gestiones", { desde, hasta, tipoGestion, clienteFiltro }],
    queryFn: () =>
      fetchVisitas({
        estado: "realizada",
        desde: desde || undefined,
        hasta: hasta || undefined,
        tipo_gestion: tipoGestion || undefined,
        cliente_id: clienteFiltro || undefined,
        per_page: 100,
      }),
  });

  const refetch = () => {
    queryClient.invalidateQueries({ queryKey: ["gestiones"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
  };

  const totalGestionesMes = resumen?.gestiones_por_tipo.reduce((acc, g) => acc + g.cantidad, 0) ?? 0;

  const columns: Column<Visita>[] = [
    { header: "Fecha", render: (v) => v.fecha },
    { header: "Cliente", render: (v) => v.cliente?.razon_social ?? "-", truncate: true },
    { header: "Tipo de gestión", render: (v) => v.tipo_gestion ?? "-", truncate: true },
    { header: "Resultado", render: (v) => v.resultado ?? "-" },
    { header: "Notas", render: (v) => v.notas_visita ?? "-", truncate: true },
    {
      header: "Acciones",
      render: (v) => (
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn btn-secondary" onClick={() => setEditando(v)}>
            Editar
          </button>
          <button className="btn btn-danger" onClick={() => setEliminando(v)}>
            Eliminar
          </button>
        </div>
      ),
    },
  ];

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
      <h2 style={{ margin: 0, color: colors.purpleDark }}>Gestiones</h2>

      {resumen && (
        <div className="dashboard-kpis">
          <div className="card">
            <div style={{ fontSize: 13, color: colors.grayNeutral }}>Total gestiones este mes</div>
            <div style={{ fontSize: 28, fontWeight: 700, color: colors.purpleDark }}>
              {totalGestionesMes}
            </div>
          </div>
          <div className="card">
            <div style={{ fontSize: 13, color: colors.grayNeutral, marginBottom: 8 }}>
              Gestiones por tipo
            </div>
            <GestionesBarList data={resumen.gestiones_por_tipo} />
          </div>
          <div
            className="card"
            style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}
          >
            <div style={{ fontSize: 13, color: colors.grayNeutral, alignSelf: "flex-start" }}>
              Cobertura de clientes
            </div>
            <DonutChart percentage={resumen.cobertura_porcentaje} />
            <div style={{ fontSize: 12, color: colors.grayNeutral, textAlign: "center" }}>
              {resumen.clientes_visitados_mes} de {resumen.total_clientes_cartera} visitados
            </div>
          </div>
          <div
            className="card"
            style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}
          >
            <div style={{ fontSize: 13, color: colors.grayNeutral, alignSelf: "flex-start" }}>
              Efectividad
            </div>
            <DonutChart percentage={resumen.efectividad_gestiones_porcentaje} color={colors.pinkNeon} />
            <div style={{ fontSize: 12, color: colors.grayNeutral, textAlign: "center" }}>
              resultó en carga de pedido
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <h3 style={{ margin: "0 0 12px", color: colors.purpleDark }}>
          Distribución de gestiones por tipo
        </h3>
        <GestionesPieChart data={resumen?.gestiones_por_tipo ?? []} />
      </div>

      <div
        className="card"
        style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "flex-end" }}
      >
        <div>
          <label htmlFor="desde">Desde</label>
          <input id="desde" type="date" value={desde} onChange={(e) => setDesde(e.target.value)} />
        </div>
        <div>
          <label htmlFor="hasta">Hasta</label>
          <input id="hasta" type="date" value={hasta} onChange={(e) => setHasta(e.target.value)} />
        </div>
        <div>
          <label htmlFor="tipo_gestion">Tipo de gestión</label>
          <select
            id="tipo_gestion"
            value={tipoGestion}
            onChange={(e) => setTipoGestion(e.target.value)}
          >
            <option value="">Todos los tipos</option>
            {TIPOS_GESTION.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="cliente">Cliente</label>
          <select
            id="cliente"
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

      <div className="card">
        <DataTable
          columns={columns}
          rows={data?.items ?? []}
          rowKey={(v) => v.id}
          loading={isLoading}
          emptyMessage="No se encontraron gestiones"
        />
      </div>

      {editando && (
        <VisitaResultadoForm
          visita={editando}
          onClose={() => setEditando(null)}
          onSaved={() => {
            setEditando(null);
            refetch();
          }}
        />
      )}

      {eliminando && (
        <ConfirmDialog
          open
          title="Eliminar gestión"
          message={`¿Seguro que deseas eliminar la gestión registrada para "${eliminando.cliente?.razon_social}"? Se eliminará la visita completa.`}
          onCancel={() => setEliminando(null)}
          onConfirm={async () => {
            try {
              await deleteVisita(eliminando.id);
              toast.success("Gestión eliminada");
              refetch();
            } catch {
              toast.error("No se pudo eliminar la gestión");
            } finally {
              setEliminando(null);
            }
          }}
        />
      )}
    </div>
  );
}
