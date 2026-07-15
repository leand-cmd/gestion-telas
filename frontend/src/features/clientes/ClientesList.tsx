import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { ImportModal } from "../../components/ImportModal";
import { Pagination } from "../../components/Pagination";
import type { Cliente } from "../../api/types";
import { colors } from "../../theme/colors";
import { ClienteForm } from "./ClienteForm";
import {
  deleteCliente,
  exportClientes,
  fetchClientes,
  importClientes,
} from "./clientesApi";

export function ClientesList() {
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Cliente | null>(null);
  const [deleting, setDeleting] = useState<Cliente | null>(null);
  const [importOpen, setImportOpen] = useState(false);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["clientes", { page, q }],
    queryFn: () => fetchClientes({ page, per_page: 10, q }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["clientes"] });

  const columns: Column<Cliente>[] = [
    { header: "ID Cliente", render: (c) => c.id },
    { header: "RUC", render: (c) => c.ruc },
    { header: "Razón Social", render: (c) => c.razon_social, truncate: true },
    { header: "Localidad", render: (c) => c.localidad ?? "-" },
    { header: "Teléfono", render: (c) => c.telefono ?? "-" },
    { header: "Email", render: (c) => c.email ?? "-", truncate: true },
    { header: "Canal", render: (c) => c.canal ?? "-" },
    { header: "Tipo Compra", render: (c) => c.tipo_compra ?? "-" },
    {
      header: "Estado",
      render: (c) => (
        <span className={`badge ${c.estado ? "badge-active" : "badge-inactive"}`}>
          {c.estado ? "Activo" : "Inactivo"}
        </span>
      ),
    },
    {
      header: "Acciones",
      render: (c) => (
        <div style={{ display: "flex", gap: 8 }}>
          <button
            className="btn btn-secondary"
            onClick={() => {
              setEditing(c);
              setFormOpen(true);
            }}
          >
            Editar
          </button>
          <button className="btn btn-danger" onClick={() => setDeleting(c)}>
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
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Clientes</h2>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <input
            placeholder="Buscar por RUC, razón social o localidad..."
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setPage(1);
            }}
            style={{ width: 280 }}
          />
          <button className="btn btn-secondary" onClick={() => setImportOpen(true)}>
            Importar
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => exportClientes().catch(() => toast.error("Error al exportar"))}
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
            + Nuevo Cliente
          </button>
        </div>
      </div>

      <div className="card">
        <DataTable
          columns={columns}
          rows={data?.items ?? []}
          rowKey={(c) => c.id}
          loading={isLoading}
          emptyMessage="No se encontraron clientes"
        />
        {data && (
          <Pagination
            page={data.page}
            pages={data.pages}
            total={data.total}
            onPageChange={setPage}
          />
        )}
      </div>

      {formOpen && (
        <ClienteForm
          cliente={editing}
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
          title="Eliminar cliente"
          message={`¿Seguro que deseas eliminar a "${deleting.razon_social}"? Esta acción no se puede deshacer.`}
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            try {
              await deleteCliente(deleting.id);
              toast.success("Cliente eliminado");
              refetch();
            } catch {
              toast.error("No se pudo eliminar el cliente");
            } finally {
              setDeleting(null);
            }
          }}
        />
      )}

      {importOpen && (
        <ImportModal
          title="Importar clientes"
          onImport={importClientes}
          onClose={() => setImportOpen(false)}
          onImported={refetch}
        />
      )}
    </div>
  );
}
