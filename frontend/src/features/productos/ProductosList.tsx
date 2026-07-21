import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { ImportModal } from "../../components/ImportModal";
import { Pagination } from "../../components/Pagination";
import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { fetchColecciones } from "../colecciones/coleccionesApi";
import { GaleriaProductos } from "./GaleriaProductos";
import { ProductoForm } from "./ProductoForm";
import {
  deleteProducto,
  exportProductos,
  fetchProductos,
  importProductos,
} from "./productosApi";

type ViewMode = "tabla" | "galeria";

export function ProductosList() {
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [view, setView] = useState<ViewMode>("tabla");
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Producto | null>(null);
  const [deleting, setDeleting] = useState<Producto | null>(null);
  const [importOpen, setImportOpen] = useState(false);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["productos", { page, q }],
    queryFn: () => fetchProductos({ page, per_page: 10, q }),
    enabled: view === "tabla",
  });

  const { data: coleccionesData } = useQuery({
    queryKey: ["colecciones"],
    queryFn: fetchColecciones,
  });
  const coleccionPorId = new Map((coleccionesData?.items ?? []).map((c) => [c.id, c]));

  const refetch = () => {
    queryClient.invalidateQueries({ queryKey: ["productos"] });
    queryClient.invalidateQueries({ queryKey: ["colecciones"] });
  };

  const abrirEditar = (p: Producto) => {
    setEditing(p);
    setFormOpen(true);
  };

  const formatPrecio = (v: number | null) => (v != null ? `₲ ${v.toLocaleString("es-PY")}` : "-");

  const columns: Column<Producto>[] = [
    { header: "Cod Producto", render: (p) => p.cod_producto },
    { header: "Marca", render: (p) => p.marca ?? "-" },
    {
      header: "Colección",
      render: (p) => (p.coleccion_id != null ? coleccionPorId.get(p.coleccion_id)?.nombre : null) ?? "-",
      truncate: true,
      minWidth: 140,
    },
    { header: "Cod Color", render: (p) => p.cod_color ?? "-" },
    {
      header: "Color Inferido",
      render: (p) => p.color_descripcion ?? "-",
      truncate: true,
      minWidth: 160,
    },
    { header: "Categoría", render: (p) => p.categoria, truncate: true, minWidth: 140 },
    { header: "Sub Categoría", render: (p) => p.sub_categoria ?? "-", truncate: true, minWidth: 140 },
    { header: "Precio Rollo", render: (p) => formatPrecio(p.precio_rollo) },
    { header: "Stock", render: (p) => p.stock_rollos ?? 0 },
    {
      header: "Activo",
      render: (p) => (
        <span className={`badge ${p.activo ? "badge-active" : "badge-inactive"}`}>
          {p.activo ? "Activo" : "Inactivo"}
        </span>
      ),
    },
    {
      header: "Acciones",
      render: (p) => (
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn btn-secondary" onClick={() => abrirEditar(p)}>
            Editar
          </button>
          <button className="btn btn-danger" onClick={() => setDeleting(p)}>
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
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Productos</h2>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <input
            placeholder="Buscar por Cod Producto o color..."
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setPage(1);
            }}
            style={{ width: 280 }}
          />
          <button
            className="btn btn-secondary"
            onClick={() => setView(view === "tabla" ? "galeria" : "tabla")}
          >
            {view === "tabla" ? "Ver galería" : "Ver tabla"}
          </button>
          <button className="btn btn-secondary" onClick={() => setImportOpen(true)}>
            Importar
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => exportProductos().catch(() => toast.error("Error al exportar"))}
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
            + Nuevo Producto
          </button>
        </div>
      </div>

      {view === "tabla" ? (
        <div className="card">
          <DataTable
            columns={columns}
            rows={data?.items ?? []}
            rowKey={(p) => p.id}
            loading={isLoading}
            emptyMessage="No se encontraron productos"
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
      ) : (
        <GaleriaProductos />
      )}

      {formOpen && (
        <ProductoForm
          producto={editing}
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
          title="Eliminar producto"
          message={`¿Seguro que deseas eliminar "${deleting.cod_producto}"? Esta acción no se puede deshacer.`}
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            try {
              await deleteProducto(deleting.id);
              toast.success("Producto eliminado");
              refetch();
            } catch {
              toast.error("No se pudo eliminar el producto");
            } finally {
              setDeleting(null);
            }
          }}
        />
      )}

      {importOpen && (
        <ImportModal
          title="Importar productos"
          onImport={importProductos}
          onClose={() => setImportOpen(false)}
          onImported={refetch}
        />
      )}
    </div>
  );
}
