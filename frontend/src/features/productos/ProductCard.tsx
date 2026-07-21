import { useRef, useState } from "react";
import toast from "react-hot-toast";

import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { uploadImagenProducto } from "./productosApi";

interface ProductCardProps {
  producto: Producto;
  onDetalle: (p: Producto) => void;
  onEditar: (p: Producto) => void;
  onUploaded: (p: Producto) => void;
}

export function ProductCard({ producto: p, onDetalle, onEditar, onUploaded }: ProductCardProps) {
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File | null) => {
    if (!file) return;
    setUploading(true);
    try {
      const actualizado = await uploadImagenProducto(p.id, file);
      onUploaded(actualizado);
      toast.success("Imagen actualizada");
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo subir la imagen");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card product-card">
      <div
        className="product-card-imagen"
        style={{
          background: p.imagen_url ? `url(${p.imagen_url}) center/cover` : colors.gradientBackground,
        }}
      />
      <div style={{ fontWeight: 700, fontSize: 14 }}>{p.cod_producto}</div>
      <div style={{ fontSize: 12, color: colors.grayNeutral, marginBottom: 8 }}>
        {p.color_general ?? "-"}
      </div>
      <div style={{ fontWeight: 600, fontSize: 13, marginBottom: 10 }}>{p.categoria || "-"}</div>
      <div style={{ display: "flex", gap: 6 }}>
        <button
          className="btn btn-secondary"
          style={{ padding: "4px 8px", fontSize: 12 }}
          onClick={() => onDetalle(p)}
          title="Ver detalle"
        >
          🔍
        </button>
        <button
          className="btn btn-secondary"
          style={{ padding: "4px 8px", fontSize: 12 }}
          onClick={() => onEditar(p)}
          title="Editar producto"
        >
          ✎
        </button>
        <button
          className="btn btn-secondary"
          style={{ padding: "4px 8px", fontSize: 12 }}
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          title="Subir foto"
        >
          {uploading ? "..." : "📷"}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          style={{ display: "none" }}
          onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
        />
      </div>
    </div>
  );
}
