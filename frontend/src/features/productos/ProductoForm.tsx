import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import {
  createProducto,
  updateProducto,
  uploadProductoImagen,
  type ProductoInput,
} from "./productosApi";

interface ProductoFormProps {
  producto: Producto | null;
  onClose: () => void;
  onSaved: () => void;
}

const EMPTY: ProductoInput = {
  cod_producto: "",
  cod_categoria: "",
  cod_color: "",
  nombre_tejido: "",
  color_general: "",
  color_descripcion: "",
  categoria: "",
  sub_categoria: "",
  composicion: "",
  ancho_cm: null,
  gramaje_gm2: null,
  precio_rollo: null,
  precio_media_rollo: null,
  precio_corte: null,
  unidad_medida: "metro",
  stock_rollos: 0,
  activo: true,
  descripcion: "",
};

export function ProductoForm({ producto, onClose, onSaved }: ProductoFormProps) {
  const [form, setForm] = useState<ProductoInput>(
    producto ? { ...EMPTY, ...producto } : EMPTY
  );
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.cod_producto.trim()) {
      toast.error("El Cod Producto es obligatorio");
      return;
    }
    if (!form.nombre_tejido.trim()) {
      toast.error("El Nombre del tejido es obligatorio");
      return;
    }
    if (!form.categoria.trim()) {
      toast.error("La Categoría es obligatoria");
      return;
    }
    setSaving(true);
    try {
      let saved: Producto;
      if (producto) {
        saved = await updateProducto(producto.id, form);
        toast.success("Producto actualizado");
      } else {
        saved = await createProducto(form);
        toast.success("Producto creado");
      }
      if (imageFile) {
        await uploadProductoImagen(saved.id, imageFile);
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
            <label htmlFor="cod_categoria">Cod Categoría</label>
            <input
              id="cod_categoria"
              value={form.cod_categoria ?? ""}
              onChange={(e) => setForm({ ...form, cod_categoria: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="nombre_tejido">Nombre Tejido</label>
            <input
              id="nombre_tejido"
              value={form.nombre_tejido}
              onChange={(e) => setForm({ ...form, nombre_tejido: e.target.value })}
              required
            />
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
            <label htmlFor="composicion">Composición</label>
            <input
              id="composicion"
              value={form.composicion ?? ""}
              onChange={(e) => setForm({ ...form, composicion: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="unidad_medida">Unidad de Medida</label>
            <input
              id="unidad_medida"
              value={form.unidad_medida ?? ""}
              onChange={(e) => setForm({ ...form, unidad_medida: e.target.value })}
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
          <div>
            <label htmlFor="imagen">Seleccionar imagen</label>
            <input
              id="imagen"
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) => setImageFile(e.target.files?.[0] ?? null)}
            />
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
