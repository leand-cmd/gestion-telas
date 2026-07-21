import { FormEvent, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import toast from "react-hot-toast";

import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { fetchColecciones } from "../colecciones/coleccionesApi";
import { createProducto, updateProducto, type ProductoInput } from "./productosApi";

interface ProductoFormProps {
  producto: Producto | null;
  onClose: () => void;
  onSaved: () => void;
}

const EMPTY: ProductoInput = {
  cod_producto: "",
  proveedor: "",
  marca: "",
  coleccion_id: null,
  cod_color: "",
  color_general: "",
  color_descripcion: "",
  categoria: "",
  sub_categoria: "",
  tipo_diseno: "",
  composicion: "",
  linea_sugerida: "",
  ancho_cm: null,
  gramaje_gm2: null,
  precio_rollo: null,
  precio_media_rollo: null,
  precio_corte: null,
  stock_rollos: 0,
  activo: true,
  descripcion: "",
};

export function ProductoForm({ producto, onClose, onSaved }: ProductoFormProps) {
  const [form, setForm] = useState<ProductoInput>(() => {
    if (!producto) return EMPTY;
    // id/created_at/updated_at son dump_only en el backend: si se
    // reenvian en el body de create/update, el schema los rechaza como
    // "Unknown field".
    const { id, created_at, updated_at, ...rest } = producto;
    return { ...EMPTY, ...rest };
  });
  const [saving, setSaving] = useState(false);

  const { data: coleccionesData } = useQuery({
    queryKey: ["colecciones"],
    queryFn: fetchColecciones,
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.cod_producto.trim()) {
      toast.error("El Cod Producto es obligatorio");
      return;
    }
    if (!form.categoria.trim()) {
      toast.error("La Categoría es obligatoria");
      return;
    }
    setSaving(true);
    try {
      if (producto) {
        await updateProducto(producto.id, form);
        toast.success("Producto actualizado");
      } else {
        await createProducto(form);
        toast.success("Producto creado");
      }
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar el producto");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay">
      <form onSubmit={handleSubmit} className="card modal-card" style={{ maxWidth: 680 }}>
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          {producto ? "Editar producto" : "Nuevo producto"}
        </h3>

        <div className="form-grid">
          <div>
            <label htmlFor="cod_producto">Cod Producto</label>
            <input
              id="cod_producto"
              value={form.cod_producto}
              onChange={(e) => setForm({ ...form, cod_producto: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="proveedor">Proveedor</label>
            <input
              id="proveedor"
              value={form.proveedor ?? ""}
              onChange={(e) => setForm({ ...form, proveedor: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="marca">Marca</label>
            <input
              id="marca"
              value={form.marca ?? ""}
              onChange={(e) => setForm({ ...form, marca: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="coleccion_id">Colección</label>
            <select
              id="coleccion_id"
              value={form.coleccion_id ?? ""}
              onChange={(e) =>
                setForm({
                  ...form,
                  coleccion_id: e.target.value ? Number(e.target.value) : null,
                })
              }
            >
              <option value="">Sin colección</option>
              {(coleccionesData?.items ?? []).map((c) => (
                <option key={c.id} value={c.id}>
                  {c.nombre}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="categoria">Categoría</label>
            <input
              id="categoria"
              value={form.categoria}
              onChange={(e) => setForm({ ...form, categoria: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="sub_categoria">Subcategoría</label>
            <input
              id="sub_categoria"
              value={form.sub_categoria ?? ""}
              onChange={(e) => setForm({ ...form, sub_categoria: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="cod_color">Cod Color</label>
            <input
              id="cod_color"
              value={form.cod_color ?? ""}
              onChange={(e) => setForm({ ...form, cod_color: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="color_general">Color General</label>
            <input
              id="color_general"
              value={form.color_general ?? ""}
              onChange={(e) => setForm({ ...form, color_general: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="color_descripcion">Color Descripción</label>
            <input
              id="color_descripcion"
              value={form.color_descripcion ?? ""}
              onChange={(e) => setForm({ ...form, color_descripcion: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="tipo_diseno">Tipo Diseño</label>
            <input
              id="tipo_diseno"
              value={form.tipo_diseno ?? ""}
              onChange={(e) => setForm({ ...form, tipo_diseno: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="composicion">Composición</label>
            <input
              id="composicion"
              value={form.composicion ?? ""}
              onChange={(e) => setForm({ ...form, composicion: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="linea_sugerida">Línea Sugerida</label>
            <input
              id="linea_sugerida"
              value={form.linea_sugerida ?? ""}
              onChange={(e) => setForm({ ...form, linea_sugerida: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="ancho_cm">Ancho (cm)</label>
            <input
              id="ancho_cm"
              type="number"
              step="0.01"
              value={form.ancho_cm ?? ""}
              onChange={(e) =>
                setForm({ ...form, ancho_cm: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div>
            <label htmlFor="gramaje_gm2">Gramaje (g/m²)</label>
            <input
              id="gramaje_gm2"
              type="number"
              step="0.01"
              value={form.gramaje_gm2 ?? ""}
              onChange={(e) =>
                setForm({ ...form, gramaje_gm2: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div>
            <label htmlFor="precio_rollo">Precio Rollo</label>
            <input
              id="precio_rollo"
              type="number"
              step="0.01"
              value={form.precio_rollo ?? ""}
              onChange={(e) =>
                setForm({ ...form, precio_rollo: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div>
            <label htmlFor="precio_media_rollo">Precio 1/2 Rollo</label>
            <input
              id="precio_media_rollo"
              type="number"
              step="0.01"
              value={form.precio_media_rollo ?? ""}
              onChange={(e) =>
                setForm({
                  ...form,
                  precio_media_rollo: e.target.value ? Number(e.target.value) : null,
                })
              }
            />
          </div>
          <div>
            <label htmlFor="precio_corte">Precio Corte</label>
            <input
              id="precio_corte"
              type="number"
              step="0.01"
              value={form.precio_corte ?? ""}
              onChange={(e) =>
                setForm({ ...form, precio_corte: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div>
            <label htmlFor="stock_rollos">Stock (rollos)</label>
            <input
              id="stock_rollos"
              type="number"
              value={form.stock_rollos ?? 0}
              onChange={(e) => setForm({ ...form, stock_rollos: Number(e.target.value) })}
            />
          </div>
          <div>
            <label htmlFor="activo">Estado</label>
            <select
              id="activo"
              value={form.activo ? "true" : "false"}
              onChange={(e) => setForm({ ...form, activo: e.target.value === "true" })}
            >
              <option value="true">Activo</option>
              <option value="false">Inactivo</option>
            </select>
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="descripcion">Descripción</label>
            <textarea
              id="descripcion"
              rows={4}
              value={form.descripcion ?? ""}
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
            />
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Guardando..." : "Guardar"}
          </button>
        </div>
      </form>
    </div>
  );
}
