import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { ConfirmDialog } from "../../components/ConfirmDialog";
import { ImportModal } from "../../components/ImportModal";
import { Pagination } from "../../components/Pagination";
import type { Coleccion, Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { ColeccionForm } from "../colecciones/ColeccionForm";
import { fetchColecciones } from "../colecciones/coleccionesApi";
import { ProductoForm } from "./ProductoForm";
import {
  deleteProducto,
  exportProductos,
  fetchProductos,
  importProductos,
} from "./productosApi";

const SIN_COLECCION = "Sin colección";

type ColeccionId = number | "none";

function ColeccionExpandida({
  coleccionId,
  onEditar,
  onEliminar,
}: {
  coleccionId: ColeccionId;
  onEditar: (p: Producto) => void;
  onEliminar: (p: Producto) => void;
}) {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ["productos-coleccion", coleccionId, page],
    queryFn: () => fetchProductos({ coleccion_id: coleccionId, page, per_page: 10 }),
  });

  const formatPrecio = (v: number | null) => (v != null ? `₲ ${v.toLocaleString("es-PY")}` : "-");

  const columnas: Column<Producto>[] = [
    { header: "Cod Producto", render: (p) => p.cod_producto },
    { header: "Color", render: (p) => p.color_general ?? "-" },
    { header: "Precio Rollo", render: (p) => formatPrecio(p.precio_rollo) },
    { header: "Stock", render: (p) => p.stock_rollos ?? 0 },
    {
      header: "Acciones",
      render: (p) => (
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn btn-secondary" onClick={() => onEditar(p)}>
            Editar
          </button>
          <button className="btn btn-danger" onClick={() => onEliminar(p)}>
            Eliminar
          </button>
        </div>
      ),
    },
  ];

  return (
    <div
      className="card"
      style={{ marginTop: 12, background: "rgba(108,93,209,0.04)" }}
      onClick={(e) => e.stopPropagation()}
    >
      <DataTable
        columns={columnas}
        rows={data?.items ?? []}
        rowKey={(p) => p.id}
        loading={isLoading}
        emptyMessage="Esta colección no tiene productos"
      />
      {data && (
        <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
      )}
    </div>
  );
}

function ColeccionCard({
  nombre,
  imagenUrl,
  count,
  expanded,
  onToggle,
  onEdit,
  onImagenClick,
}: {
  nombre: string;
  imagenUrl: string | null;
  count: number;
  expanded: boolean;
  onToggle: () => void;
  onEdit?: () => void;
  onImagenClick: () => void;
}) {
  return (
    <div
      className="card coleccion-card"
      style={{ border: expanded ? `2px solid ${colors.purplePrimary}` : undefined }}
      onClick={onToggle}
    >
      <div
        className="coleccion-card-imagen"
        style={{
          background: imagenUrl ? `url(${imagenUrl}) center/cover` : colors.gradientBackground,
        }}
        onClick={(e) => {
          if (!imagenUrl) return;
          e.stopPropagation();
          onImagenClick();
        }}
      />
      <div style={{ fontWeight: 700, fontSize: 15 }}>{nombre}</div>
      <div style={{ fontSize: 12, color: colors.grayNeutral, marginBottom: 8 }}>
        {count} {count === 1 ? "producto" : "productos"}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        {imagenUrl && (
          <button
            className="btn btn-secondary"
            style={{ padding: "4px 10px", fontSize: 13 }}
            onClick={(e) => {
              e.stopPropagation();
              onImagenClick();
            }}
            title="Ver imagen completa"
          >
            🔍
          </button>
        )}
        {onEdit && (
          <button
            className="btn btn-secondary"
            style={{ padding: "4px 10px", fontSize: 13 }}
            onClick={(e) => {
              e.stopPropagation();
              onEdit();
            }}
            title="Editar colección"
          >
            ✎
          </button>
        )}
        <button
          className="btn btn-secondary"
          style={{ padding: "4px 10px", fontSize: 13, marginLeft: "auto" }}
          onClick={(e) => {
            e.stopPropagation();
            onToggle();
          }}
          title={expanded ? "Colapsar" : "Expandir"}
        >
          {expanded ? "−" : "+"}
        </button>
      </div>
    </div>
  );
}

type ViewMode = "tabla" | "galeria";

export function ProductosList() {
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [view, setView] = useState<ViewMode>("tabla");
  const [expandedColeccion, setExpandedColeccion] = useState<ColeccionId | null>(null);
  const [editingColeccion, setEditingColeccion] = useState<Coleccion | null>(null);
  const [imagenExpandida, setImagenExpandida] = useState<string | null>(null);
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
    queryClient.invalidateQueries({ queryKey: ["productos-coleccion"] });
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

  const tarjetas: { id: ColeccionId; coleccion: Coleccion | null; count: number }[] = [
    ...(coleccionesData?.items ?? []).map((c) => ({
      id: c.id as ColeccionId,
      coleccion: c,
      count: c.productos_count ?? 0,
    })),
    { id: "none" as ColeccionId, coleccion: null, count: coleccionesData?.sin_coleccion_count ?? 0 },
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
        <div className="colecciones-grid">
          {tarjetas.map(({ id, coleccion, count }) => (
            <div key={id} className="coleccion-wrapper">
              <ColeccionCard
                nombre={coleccion?.nombre ?? SIN_COLECCION}
                imagenUrl={coleccion?.imagen_url ?? null}
                count={count}
                expanded={expandedColeccion === id}
                onToggle={() => setExpandedColeccion(expandedColeccion === id ? null : id)}
                onEdit={coleccion ? () => setEditingColeccion(coleccion) : undefined}
                onImagenClick={() => setImagenExpandida(coleccion?.imagen_url ?? null)}
              />
              {expandedColeccion === id && (
                <div className="productos-expandidos">
                  <ColeccionExpandida
                    coleccionId={id}
                    onEditar={abrirEditar}
                    onEliminar={setDeleting}
                  />
                </div>
              )}
            </div>
          ))}
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

      {editingColeccion && (
        <ColeccionForm
          coleccion={editingColeccion}
          onClose={() => setEditingColeccion(null)}
          onSaved={() => {
            setEditingColeccion(null);
            queryClient.invalidateQueries({ queryKey: ["colecciones"] });
          }}
        />
      )}

      {imagenExpandida && (
        <div className="lightbox-overlay" onClick={() => setImagenExpandida(null)}>
          <img src={imagenExpandida} alt="Imagen completa" className="lightbox-imagen" />
        </div>
      )}
    </div>
  );
}
