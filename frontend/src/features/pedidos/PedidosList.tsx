import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { Pagination } from "../../components/Pagination";
import type { Pedido, PedidoEstado } from "../../api/types";
import { colors } from "../../theme/colors";
import { PedidoForm } from "./PedidoForm";
import {
  cambiarEstadoPedido,
  convertirPedidoAVenta,
  deletePedido,
  descargarPdfPedido,
  enviarEmailPedido,
  exportPedidos,
  fetchPedidos,
} from "./pedidosApi";

const TRANSICIONES: Record<PedidoEstado, PedidoEstado[]> = {
  Pendiente: ["Confirmado", "Cancelado"],
  Confirmado: ["Entregado", "Cancelado"],
  Entregado: ["Cancelado"],
  Facturado: [],
  Cancelado: [],
};

const ESTADOS_FILTRO: PedidoEstado[] = [
  "Pendiente",
  "Confirmado",
  "Entregado",
  "Facturado",
  "Cancelado",
];

export function PedidosList() {
  const [page, setPage] = useState(1);
  const [estado, setEstado] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Pedido | null>(null);
  const [deleting, setDeleting] = useState<Pedido | null>(null);
  const [convirtiendo, setConvirtiendo] = useState<Pedido | null>(null);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["pedidos", { page, estado }],
    queryFn: () => fetchPedidos({ page, per_page: 10, estado: estado || undefined }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["pedidos"] });

  const columns: Column<Pedido>[] = [
    { header: "Nro. Pedido", render: (p) => p.nro_pedido },
    { header: "Cliente", render: (p) => p.cliente?.razon_social ?? "-", truncate: true },
    { header: "Fecha", render: (p) => p.fecha_pedido ?? "-" },
    {
      header: "Total",
      render: (p) => `₲ ${p.total.toLocaleString("es-PY")}`,
    },
    {
      header: "Estado",
      render: (p) => <span className="badge badge-active">{p.estado}</span>,
    },
    {
      header: "Acciones",
      render: (p) => (
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          {p.estado === "Pendiente" && (
            <button
              className="btn btn-secondary"
              onClick={() => {
                setEditing(p);
                setFormOpen(true);
              }}
            >
              Editar
            </button>
          )}
          {TRANSICIONES[p.estado].map((siguiente) => (
            <button
              key={siguiente}
              className="btn btn-secondary"
              onClick={async () => {
                try {
                  await cambiarEstadoPedido(p.id, siguiente);
                  toast.success(`Pedido pasado a ${siguiente}`);
                  refetch();
                } catch {
                  toast.error("No se pudo cambiar el estado");
                }
              }}
            >
              {siguiente}
            </button>
          ))}
          {(p.estado === "Confirmado" || p.estado === "Entregado") && (
            <button className="btn btn-primary" onClick={() => setConvirtiendo(p)}>
              Convertir a venta
            </button>
          )}
          <button
            className="btn btn-secondary"
            onClick={() =>
              descargarPdfPedido(p.id, p.nro_pedido).catch(() => toast.error("Error al generar PDF"))
            }
          >
            PDF
          </button>
          <button
            className="btn btn-secondary"
            onClick={() =>
              enviarEmailPedido(p.id)
                .then(() => toast.success("Email enviado"))
                .catch((err) => toast.error(err?.response?.data?.error || "Error al enviar email"))
            }
          >
            Email
          </button>
          {p.estado === "Pendiente" && (
            <button className="btn btn-danger" onClick={() => setDeleting(p)}>
              Eliminar
            </button>
          )}
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
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Pedidos</h2>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <select
            value={estado}
            onChange={(e) => {
              setEstado(e.target.value);
              setPage(1);
            }}
          >
            <option value="">Todos los estados</option>
            {ESTADOS_FILTRO.map((e) => (
              <option key={e} value={e}>
                {e}
              </option>
            ))}
          </select>
          <button
            className="btn btn-secondary"
            onClick={() => exportPedidos().catch(() => toast.error("Error al exportar"))}
          >
            Exportar CSV
          </button>
          <button
            className="btn btn-primary"
            onClick={() => {
              setEditing(null);
              setFormOpen(true);
            }}
          >
            + Nuevo Pedido
          </button>
        </div>
      </div>

      <div className="card">
        <DataTable
          columns={columns}
          rows={data?.items ?? []}
          rowKey={(p) => p.id}
          loading={isLoading}
          emptyMessage="No se encontraron pedidos"
        />
        {data && (
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        )}
      </div>

      {formOpen && (
        <PedidoForm
          pedido={editing}
          onClose={() => setFormOpen(false)}
          onSaved={() => {
            setFormOpen(false);
            refetch();
          }}
        />
      )}

      {deleting && (
        <ConfirmDialog
          open
          title="Eliminar pedido"
          message={`¿Seguro que deseas eliminar el pedido "${deleting.nro_pedido}"?`}
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            try {
              await deletePedido(deleting.id);
              toast.success("Pedido eliminado");
              refetch();
            } catch {
              toast.error("No se pudo eliminar el pedido");
            } finally {
              setDeleting(null);
            }
          }}
        />
      )}

      {convirtiendo && (
        <ConfirmDialog
          open
          title="Convertir a venta"
          message={`¿Generar una venta a partir del pedido "${convirtiendo.nro_pedido}"? Esta acción no se puede deshacer.`}
          confirmLabel="Convertir"
          onCancel={() => setConvirtiendo(null)}
          onConfirm={async () => {
            try {
              await convertirPedidoAVenta(convirtiendo.id);
              toast.success("Venta generada");
              refetch();
              queryClient.invalidateQueries({ queryKey: ["ventas"] });
            } catch (err: any) {
              toast.error(err?.response?.data?.error || "No se pudo convertir el pedido");
            } finally {
              setConvirtiendo(null);
            }
          }}
        />
      )}
    </div>
  );
}
