import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { CATEGORIAS, CLASES, ORIGENES } from "./productoOptions";
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
  cod_sku: "",
  nro_producto: null,
  descripcion: "",
  clase: "",
  categoria: "",
  origen: "",
  metros: null,
  kilogramos: null,
  piezas: null,
  color: "#6C5DD1",
  marca: "",
  precio: null,
  costo: null,
  stock_actual: 0,
  stock_minimo: 0,
  estado: true,
};

export function ProductoForm({ producto, onClose, onSaved }: ProductoFormProps) {
  const [form, setForm] = useState<ProductoInput>(
    producto ? { ...EMPTY, ...producto } : EMPTY
  );
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
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
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(43,43,56,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        overflowY: "auto",
        padding: 24,
      }}
    >
      <form
        onSubmit={handleSubmit}
        className="card"
        style={{ width: "100%", maxWidth: 680, display: "flex", flexDirection: "column", gap: 14 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          {producto ? "Editar producto" : "Nuevo producto"}
        </h3>

        <div className="form-grid">
          <div>
            <label htmlFor="cod_sku">Cod SKU</label>
            <input
              id="cod_sku"
              value={form.cod_sku}
              onChange={(e) => setForm({ ...form, cod_sku: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="nro_producto">Nro Producto</label>
            <input
              id="nro_producto"
              type="number"
              value={form.nro_producto ?? ""}
              onChange={(e) =>
                setForm({ ...form, nro_producto: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="descripcion">Descripción</label>
            <textarea
              id="descripcion"
              rows={2}
              value={form.descripcion ?? ""}
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="clase">Clase</label>
            <select
              id="clase"
              value={form.clase ?? ""}
              onChange={(e) => setForm({ ...form, clase: e.target.value })}
            >
              <option value="">Seleccionar...</option>
              {CLASES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
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
            <label htmlFor="origen">Origen</label>
            <select
              id="origen"
              value={form.origen ?? ""}
              onChange={(e) => setForm({ ...form, origen: e.target.value })}
            >
              <option value="">Seleccionar...</option>
              {ORIGENES.map((o) => (
                <option key={o} value={o}>
                  {o}
                </option>
              ))}
            </select>
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
            <label htmlFor="metros">Metros</label>
            <input
              id="metros"
              type="number"
              step="0.001"
              value={form.metros ?? ""}
              onChange={(e) =>
                setForm({ ...form, metros: e.target.value ? Number(e.target.value) : null })
              }
            />
          </div>
          <div>
            <label htmlFor="kilogramos">Kilogramos</label>
            <input
              id="kilogramos"
              type="number"
              step="0.001"
              value={form.kilogramos ?? ""}
              onChange={(e) =>
                setForm({ ...form, kilogramos: e.target.value ? Number(e.target.value) : null })
              }
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
            <label htmlFor="color">Color</label>
            <div style={{ display: "flex", gap: 8 }}>
              <input
                id="color"
                type="color"
                style={{ width: 48, padding: 2 }}
                value={/^#/.test(form.color ?? "") ? (form.color as string) : "#6C5DD1"}
                onChange={(e) => setForm({ ...form, color: e.target.value })}
              />
              <input
                aria-label="Nombre del color"
                placeholder="Nombre del color"
                value={form.color ?? ""}
                onChange={(e) => setForm({ ...form, color: e.target.value })}
              />
            </div>
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
            <label htmlFor="costo">Costo</label>
            <input
              id="costo"
              type="number"
              step="0.01"
              value={form.costo ?? ""}
              onChange={(e) =>
                setForm({ ...form, costo: e.target.value ? Number(e.target.value) : null })
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
            <label htmlFor="imagen">Imagen del producto</label>
            <input
              id="imagen"
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) => setImageFile(e.target.files?.[0] ?? null)}
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
