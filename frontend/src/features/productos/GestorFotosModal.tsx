import { DragEvent, useRef, useState } from "react";
import toast from "react-hot-toast";

import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";
import { deleteImagenProducto, uploadImagenProducto } from "./productosApi";

interface GestorFotosModalProps {
  producto: Producto;
  onClose: () => void;
  onChanged: (p: Producto) => void;
}

export function GestorFotosModal({ producto, onClose, onChanged }: GestorFotosModalProps) {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File | null) => {
    if (!file) return;
    setUploading(true);
    try {
      const actualizado = await uploadImagenProducto(producto.id, file);
      onChanged(actualizado);
      toast.success("Foto actualizada");
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo subir la imagen");
    } finally {
      setUploading(false);
    }
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files?.[0] ?? null);
  };

  const handleEliminar = async () => {
    try {
      const actualizado = await deleteImagenProducto(producto.id);
      onChanged(actualizado);
      toast.success("Foto eliminada");
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo eliminar la foto");
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="card modal-card" style={{ maxWidth: 420 }} onClick={(e) => e.stopPropagation()}>
        <h3 style={{ margin: 0, color: colors.purpleDark }}>Foto de {producto.cod_producto}</h3>

        {producto.imagen_url && (
          <img
            src={producto.imagen_url}
            alt={producto.cod_producto}
            style={{ width: "100%", height: 180, objectFit: "cover", borderRadius: 16 }}
          />
        )}

        <div
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          style={{
            border: `2px dashed ${dragOver ? colors.purplePrimary : "#e3e1f0"}`,
            borderRadius: 16,
            padding: 16,
            textAlign: "center",
            cursor: "pointer",
            background: dragOver ? "rgba(108,93,209,0.06)" : "transparent",
          }}
        >
          <div style={{ fontSize: 13, color: colors.grayNeutral }}>
            {uploading ? "Subiendo..." : "Arrastrá una imagen aquí o hacé clic para cambiar la foto"}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/png,image/jpeg,image/webp"
            style={{ display: "none" }}
            onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
          />
        </div>

        <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
          {producto.imagen_url ? (
            <button type="button" className="btn btn-danger" onClick={handleEliminar}>
              Eliminar foto
            </button>
          ) : (
            <span />
          )}
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}
