import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { Pagination } from "../../components/Pagination";
import type { Venta, VentaEstadoPago } from "../../api/types";
import { colors } from "../../theme/colors";
import { VentaForm } from "./VentaForm";
import { cambiarEstadoPago, descargarPdfVenta, exportVentas, fetchVentas } from "./ventasApi";

const ESTADOS_PAGO: VentaEstadoPago[] = ["pendiente", "pagado", "vencido"];

export function VentasList() {
  const [page, setPage] = useState(1);
  const [estadoPago, setEstadoPago] = useState("");
  const [formOpen, setFormOpen] = useState(false);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["ventas", { page, estadoPago }],
    queryFn: () => fetchVentas({ page, per_page: 10, estado_pago: estadoPago || undefined }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["ventas"] });

  const columns: Column<Venta>[] = [
    { header: "Nro. Factura", render: (v) => v.nro_factura },
    { header: "Cliente", render: (v) => v.cliente?.razon_social ?? "-" },
    { header: "Fecha", render: (v) => v.fecha_factura ?? "-" },
    { header: "Total", render: (v) => `₲ ${v.total.toLocaleString("es-PY")}` },
    {
      header: "Estado de pago",
      render: (v) => (
        <select
          value={v.estado_pago}
          onChange={async (e) => {
            try {
              await cambiarEstadoPago(v.id, e.target.value as VentaEstadoPago);
              toast.success("Estado de pago actualizado");
              refetch();
            } catch {
              toast.error("No se pudo actualizar el estado de pago");
            }
          }}
        >
          {ESTADOS_PAGO.map((e) => (
            <option key={e} value={e}>
              {e}
            </option>
          ))}
        </select>
      ),
    },
    {
      header: "Acciones",
      render: (v) => (
        <button
          className="btn btn-secondary"
          onClick={() =>
            descargarPdfVenta(v.id, v.nro_factura).catch(() => toast.error("Error al generar PDF"))
          }
        >
          PDF
        </button>
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
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Ventas</h2>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <select
            value={estadoPago}
            onChange={(e) => {
              setEstadoPago(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Todos los estados de pago</option>
            {ESTADOS_PAGO.map((e) => (
              <option key={e} value={e}>
                {e}
              </option>
            ))}
          </select>
          <button
            className="btn btn-secondary"
            onClick={() => exportVentas().catch(() => toast.error("Error al exportar"))}
          >
            Exportar CSV
          </button>
          <button className="btn btn-primary" onClick={() => setFormOpen(true)}>
            + Nueva Venta
          </button>
        </div>
      </div>

      <div className="card">
        <DataTable
          columns={columns}
          rows={data?.items ?? []}
          rowKey={(v) => v.id}
          loading={isLoading}
          emptyMessage="No se encontraron ventas"
        />
        {data && (
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        )}
      </div>

      {formOpen && (
        <VentaForm
          onClose={() => setFormOpen(false)}
          onSaved={() => {
            setFormOpen(false);
            refetch();
          }}
        />
      )}
    </div>
  );
}
