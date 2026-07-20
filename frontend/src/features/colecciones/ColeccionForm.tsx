import { DragEvent, FormEvent, useRef, useState } from "react";
import toast from "react-hot-toast";

import type { Coleccion } from "../../api/types";
import { colors } from "../../theme/colors";
import {
  createColeccion,
  updateColeccion,
  uploadImagenColeccion,
  type ColeccionInput,
} from "./coleccionesApi";

interface ColeccionFormProps {
  coleccion: Coleccion | null;
  /** Si viene seteado, el campo Nombre queda fijo (no editable) en este valor
   * — usado cuando se abre el formulario desde una tarjeta de tejido, donde
   * el nombre debe coincidir exactamente para que la foto se enganche. */
  nombreFijo?: string;
  onClose: () => void;
  onSaved: () => void;
}

export function ColeccionForm({ coleccion, nombreFijo, onClose, onSaved }: ColeccionFormProps) {
  const [form, setForm] = useState<ColeccionInput>({
    nombre: coleccion?.nombre ?? nombreFijo ?? "",
    descripcion: coleccion?.descripcion ?? "",
    imagen_url: coleccion?.imagen_url ?? null,
  });
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [saving, setSaving] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File | null) => {
    if (!file) return;
    setUploading(true);
    try {
      const url = await uploadImagenColeccion(file);
      setForm((prev) => ({ ...prev, imagen_url: url }));
      toast.success("Imagen subida");
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

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.nombre.trim()) {
      toast.error("El nombre es obligatorio");
      return;
    }
    setSaving(true);
    try {
      if (coleccion) {
        await updateColeccion(coleccion.id, form);
        toast.success("Colección actualizada");
      } else {
        await createColeccion(form);
        toast.success("Colección creada");
      }
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar la colección");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay">
      <form onSubmit={handleSubmit} className="card modal-card" style={{ maxWidth: 460 }}>
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          {coleccion ? "Editar colección" : "Nueva colección"}
        </h3>

        <div>
          <label htmlFor="nombre">Nombre</label>
          <input
            id="nombre"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            disabled={!!nombreFijo}
            required
          />
        </div>
        <div>
          <label htmlFor="descripcion">Descripción</label>
          <textarea
            id="descripcion"
            rows={3}
            value={form.descripcion ?? ""}
            onChange={(e) => setForm({ ...form, descripcion: e.target.value })}
          />
        </div>

        <div>
          <label>Imagen</label>
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
            {form.imagen_url ? (
              <img
                src={form.imagen_url}
                alt="Vista previa"
                style={{ height: 90, borderRadius: 10, objectFit: "cover" }}
              />
            ) : (
              <div style={{ fontSize: 13, color: colors.grayNeutral, padding: "12px 0" }}>
                {uploading ? "Subiendo..." : "Arrastrá una imagen aquí o hacé clic para elegir"}
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg,image/webp"
              style={{ display: "none" }}
              onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
            />
          </div>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving || uploading}>
            {saving ? "Guardando..." : "Guardar"}
          </button>
        </div>
      </form>
    </div>
  );
}
