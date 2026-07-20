import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { ImportModal } from "../../components/ImportModal";
import { Pagination } from "../../components/Pagination";
import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
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
    queryFn: () => fetchProductos({ page, per_page: view === "galeria" ? 12 : 10, q }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["productos"] });

  const formatPrecio = (v: number | null) => (v != null ? `₲ ${v.toLocaleString("es-PY")}` : "-");

  const columns: Column<Producto>[] = [
    { header: "Cod Producto", render: (p) => p.cod_producto },
    { header: "Marca", render: (p) => p.marca ?? "-" },
    { header: "Colección", render: (p) => p.coleccion ?? "-", truncate: true, minWidth: 140 },
    { header: "Nombre Tejido", render: (p) => p.nombre_tejido, truncate: true, minWidth: 160 },
    { header: "Cod Color", render: (p) => p.cod_color ?? "-" },
    {
      header: "Color Inferido",
      render: (p) => p.color_descripcion ?? "-",
      truncate: true,
      minWidth: 160,
    },
    { header: "Color General", render: (p) => p.color_general ?? "-" },
    { header: "Categoría", render: (p) => p.categoria, truncate: true, minWidth: 140 },
    { header: "Sub Categoría", render: (p) => p.sub_categoria ?? "-", truncate: true, minWidth: 140 },
    { header: "Tipo Diseño", render: (p) => p.tipo_diseno ?? "-" },
    { header: "Composicion", render: (p) => p.composicion ?? "-", truncate: true, minWidth: 160 },
    {
      header: "Línea Sugerida",
      render: (p) => p.linea_sugerida ?? "-",
      truncate: true,
      minWidth: 160,
    },
    { header: "Rollo", render: (p) => formatPrecio(p.precio_rollo) },
    { header: "1/2 Rollo", render: (p) => formatPrecio(p.precio_media_rollo) },
    { header: "Corte", render: (p) => formatPrecio(p.precio_corte) },
    { header: "Ancho", render: (p) => (p.ancho_cm != null ? `${p.ancho_cm} cm` : "-") },
    { header: "Gramaje", render: (p) => (p.gramaje_gm2 != null ? `${p.gramaje_gm2} g/m²` : "-") },
    { header: "Stock", render: (p) => p.stock_rollos ?? 0 },
    {
      header: "Activo",
      render: (p) => (
        <span className={`badge ${p.activo ? "badge-active" : "badge-inactive"}`}>
          {p.activo ? "Activo" : "Inactivo"}
        </span>
      ),
    },
    { header: "Fecha Creación", render: (p) => p.fecha_creacion ?? "-" },
    {
      header: "Acciones",
      render: (p) => (
        <div style={{ display: "flex", gap: 8 }}>
          <button
            className="btn btn-secondary"
            onClick={() => {
              setEditing(p);
              setFormOpen(true);
            }}
          >
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
            placeholder="Buscar por Cod Producto, tejido o color..."
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
        <div>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))",
              gap: 16,
            }}
          >
            {(data?.items ?? []).map((p) => (
              <div
                key={p.id}
                className="card"
                style={{ padding: 16, cursor: "pointer" }}
                onClick={() => {
                  setEditing(p);
                  setFormOpen(true);
                }}
              >
                <div
                  style={{
                    width: "100%",
                    height: 140,
                    borderRadius: 16,
                    background: p.url_imagen
                      ? `url(${p.url_imagen}) center/cover`
                      : colors.gradientBackground,
                    marginBottom: 12,
                  }}
                />
                <div style={{ fontWeight: 700, fontSize: 14 }}>{p.cod_producto}</div>
                <div style={{ fontSize: 12, color: colors.grayNeutral, marginBottom: 6 }}>
                  {p.nombre_tejido}
                </div>
                <div style={{ fontSize: 12 }}>{p.color_general ?? "-"}</div>
              </div>
            ))}
          </div>
          {data && (
            <Pagination
              page={data.page}
              pages={data.pages}
              total={data.total}
              onPageChange={setPage}
            />
          )}
        </div>
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
