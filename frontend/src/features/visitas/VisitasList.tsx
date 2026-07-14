import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { Pagination } from "../../components/Pagination";
import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { VisitaForm } from "./VisitaForm";
import { VisitaResultadoForm } from "./VisitaResultadoForm";
import { deleteVisita, fetchVisitas } from "./visitasApi";

export function VisitasList() {
  const [page, setPage] = useState(1);
  const [desde, setDesde] = useState("");
  const [hasta, setHasta] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [registrandoResultado, setRegistrandoResultado] = useState<Visita | null>(null);
  const [deleting, setDeleting] = useState<Visita | null>(null);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["visitas", { page, desde, hasta }],
    queryFn: () =>
      fetchVisitas({ page, per_page: 10, desde: desde || undefined, hasta: hasta || undefined }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["visitas"] });

  const columns: Column<Visita>[] = [
    { header: "Fecha", render: (v) => v.fecha },
    { header: "Hora", render: (v) => v.hora },
    { header: "Cliente", render: (v) => v.cliente?.razon_social ?? "-" },
    { header: "Asesor", render: (v) => v.asesor?.nombre ?? "-" },
    { header: "Propósito", render: (v) => v.proposito ?? "-" },
    {
      header: "Estado",
      render: (v) => (
        <span className={`badge ${v.estado === "realizada" ? "badge-active" : "badge-inactive"}`}>
          {v.estado}
        </span>
      ),
    },
    {
      header: "Acciones",
      render: (v) => (
        <div style={{ display: "flex", gap: 8 }}>
          {v.estado === "programada" && (
            <button className="btn btn-primary" onClick={() => setRegistrandoResultado(v)}>
              Registrar resultado
            </button>
          )}
          <button className="btn btn-danger" onClick={() => setDeleting(v)}>
            Eliminar
          </button>
        </div>
      ),
    },
  ];

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
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
          <input
            type="date"
            value={desde}
            onChange={(e) => {
              setDesde(e.target.value);
              setPage(1);
            }}
          />
          <input
            type="date"
            value={hasta}
            onChange={(e) => {
              setHasta(e.target.value);
              setPage(1);
            }}
          />
          <button className="btn btn-primary" onClick={() => setFormOpen(true)}>
            + Programar Visita
          </button>
        </div>
      </div>

      <div className="card">
        <DataTable
          columns={columns}
          rows={data?.items ?? []}
          rowKey={(v) => v.id}
          loading={isLoading}
          emptyMessage="No se encontraron visitas"
        />
        {data && (
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        )}
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

      {deleting && (
        <ConfirmDialog
          open
          title="Eliminar visita"
          message={`¿Seguro que deseas eliminar la visita del ${deleting.fecha}?`}
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            try {
              await deleteVisita(deleting.id);
              toast.success("Visita eliminada");
              refetch();
            } catch {
              toast.error("No se pudo eliminar la visita");
            } finally {
              setDeleting(null);
            }
          }}
        />
      )}
    </div>
  );
}
