import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import type { Coleccion, Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { ColeccionForm } from "../colecciones/ColeccionForm";
import { ColeccionCard } from "./ColeccionCard";
import { ProductCard } from "./ProductCard";
import { ProductDetailModal } from "./ProductDetailModal";
import { ProductoForm } from "./ProductoForm";
import { fetchColeccionesConProductos } from "./productosApi";

type ColeccionKey = number | "none";

export function GaleriaProductos() {
  const [expandida, setExpandida] = useState<ColeccionKey | null>(null);
  const [editingColeccion, setEditingColeccion] = useState<Coleccion | null>(null);
  const [imagenExpandida, setImagenExpandida] = useState<string | null>(null);
  const [detalleProducto, setDetalleProducto] = useState<Producto | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Producto | null>(null);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["colecciones-con-productos"],
    queryFn: fetchColeccionesConProductos,
  });

  const refetch = () => {
    queryClient.invalidateQueries({ queryKey: ["colecciones-con-productos"] });
    queryClient.invalidateQueries({ queryKey: ["colecciones"] });
  };

  const abrirEditar = (p: Producto) => {
    setEditing(p);
    setFormOpen(true);
  };

  if (isLoading) {
    return (
      <div style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>Cargando...</div>
    );
  }

  const grupos = data ?? [];

  return (
    <div>
      <div className="colecciones-grid">
        {grupos.map((grupo) => {
          const key: ColeccionKey = grupo.id ?? "none";
          const esColeccionReal = grupo.id != null;
          return (
            <div key={key} className="coleccion-wrapper">
              <ColeccionCard
                nombre={grupo.nombre}
                imagenUrl={grupo.imagen_url}
                count={grupo.productos.length}
                expanded={expandida === key}
                onToggle={() => setExpandida(expandida === key ? null : key)}
                onEdit={
                  esColeccionReal
                    ? () =>
                        setEditingColeccion({
                          id: grupo.id as number,
                          nombre: grupo.nombre,
                          descripcion: grupo.descripcion,
                          imagen_url: grupo.imagen_url,
                          created_at: "",
                          updated_at: "",
                        })
                    : undefined
                }
                onImagenClick={() => setImagenExpandida(grupo.imagen_url)}
              />
              {expandida === key && (
                <div className="productos-expandidos">
                  {grupo.productos.length === 0 ? (
                    <div
                      className="card"
                      style={{ padding: 24, textAlign: "center", color: colors.grayNeutral }}
                    >
                      Esta colección no tiene productos
                    </div>
                  ) : (
                    <div className="productos-grid">
                      {grupo.productos.map((p) => (
                        <ProductCard
                          key={p.id}
                          producto={p}
                          onDetalle={setDetalleProducto}
                          onEditar={abrirEditar}
                          onUploaded={refetch}
                        />
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

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

      {editingColeccion && (
        <ColeccionForm
          coleccion={editingColeccion}
          onClose={() => setEditingColeccion(null)}
          onSaved={() => {
            setEditingColeccion(null);
            refetch();
          }}
        />
      )}

      {imagenExpandida && (
        <div className="lightbox-overlay" onClick={() => setImagenExpandida(null)}>
          <img src={imagenExpandida} alt="Imagen completa" className="lightbox-imagen" />
        </div>
      )}

      {detalleProducto && (
        <ProductDetailModal producto={detalleProducto} onClose={() => setDetalleProducto(null)} />
      )}
    </div>
  );
}
