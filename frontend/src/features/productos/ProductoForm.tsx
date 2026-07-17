import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { CATEGORIAS } from "./productoOptions";
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
  marca: "",
  linea: "",
  categoria: "",
  subcategoria: "",
  cod_color: "",
  color: "",
  color_categoria: "",
  codigo_base: "",
  descripcion_completa: "",
  diseno: "",
  medida: "",
  piezas: null,
  precio: null,
  stock_actual: 0,
  stock_minimo: 0,
  estado: true,
  origen: "",
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
            <label htmlFor="marca">Marca</label>
            <input
              id="marca"
              value={form.marca ?? ""}
              onChange={(e) => setForm({ ...form, marca: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="linea">Línea</label>
            <input
              id="linea"
              value={form.linea ?? ""}
              onChange={(e) => setForm({ ...form, linea: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="categoria">Categoría</label>
            <select
              id="categoria"
              value={form.categoria ?? ""}
              onChange={(e) => setForm({ ...form, categoria: e.target.value })}
            >
              <option value="">Seleccionar...</option>
              {CATEGORIAS.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="subcategoria">Subcategoría</label>
            <input
              id="subcategoria"
              value={form.subcategoria ?? ""}
              onChange={(e) => setForm({ ...form, subcategoria: e.target.value })}
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
            <label htmlFor="color">Color</label>
            <input
              id="color"
              value={form.color ?? ""}
              onChange={(e) => setForm({ ...form, color: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="color_categoria">Color Categoría</label>
            <input
              id="color_categoria"
              value={form.color_categoria ?? ""}
              onChange={(e) => setForm({ ...form, color_categoria: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="codigo_base">Código Base</label>
            <input
              id="codigo_base"
              value={form.codigo_base ?? ""}
              onChange={(e) => setForm({ ...form, codigo_base: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="diseno">Diseño</label>
            <input
              id="diseno"
              value={form.diseno ?? ""}
              onChange={(e) => setForm({ ...form, diseno: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="medida">Medida</label>
            <input
              id="medida"
              value={form.medida ?? ""}
              onChange={(e) => setForm({ ...form, medida: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="origen">Origen</label>
            <input
              id="origen"
              value={form.origen ?? ""}
              onChange={(e) => setForm({ ...form, origen: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="piezas">Piezas</label>
            <input
              id="piezas"
              type="number"
              value={form.piezas ?? ""}
              onChange={(e) =>
                setForm({ ...form, piezas: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div>
            <label htmlFor="precio">Precio</label>
            <input
              id="precio"
              type="number"
              step="0.01"
              value={form.precio ?? ""}
              onChange={(e) =>
                setForm({ ...form, precio: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div>
            <label htmlFor="stock_actual">Stock Actual</label>
            <input
              id="stock_actual"
              type="number"
              value={form.stock_actual}
              onChange={(e) => setForm({ ...form, stock_actual: Number(e.target.value) })}
            />
          </div>
          <div>
            <label htmlFor="stock_minimo">Stock Mínimo</label>
            <input
              id="stock_minimo"
              type="number"
              value={form.stock_minimo ?? 0}
              onChange={(e) => setForm({ ...form, stock_minimo: Number(e.target.value) })}
            />
          </div>
          <div>
            <label htmlFor="estado">Estado</label>
            <select
              id="estado"
              value={form.estado ? "true" : "false"}
              onChange={(e) => setForm({ ...form, estado: e.target.value === "true" })}
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
            <label htmlFor="descripcion_completa">Descripción Completa</label>
            <textarea
              id="descripcion_completa"
              rows={4}
              value={form.descripcion_completa ?? ""}
              onChange={(e) => setForm({ ...form, descripcion_completa: e.target.value })}
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
