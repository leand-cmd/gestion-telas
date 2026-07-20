import { DragEvent, FormEvent, useRef, useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { ConfirmDialog } from "../../components/ConfirmDialog";
import type { Coleccion } from "../../api/types";
import { colors } from "../../theme/colors";
import {
  createColeccion,
  deleteColeccion,
  fetchColecciones,
  updateColeccion,
  uploadImagenColeccion,
  type ColeccionInput,
} from "./coleccionesApi";

const EMPTY: ColeccionInput = {
  nombre: "",
  descripcion: "",
  imagen_url: null,
};

export function ColeccionesManager() {
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Coleccion | null>(null);
  const [deleting, setDeleting] = useState<Coleccion | null>(null);
  const [form, setForm] = useState<ColeccionInput>(EMPTY);
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [saving, setSaving] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["colecciones"],
    queryFn: fetchColecciones,
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["colecciones"] });

  const openCreate = () => {
    setEditing(null);
    setForm(EMPTY);
    setFormOpen(true);
  };

  const openEdit = (c: Coleccion) => {
    setEditing(c);
    setForm({ nombre: c.nombre, descripcion: c.descripcion, imagen_url: c.imagen_url });
    setFormOpen(true);
  };

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
      if (editing) {
        await updateColeccion(editing.id, form);
        toast.success("Colección actualizada");
      } else {
        await createColeccion(form);
        toast.success("Colección creada");
      }
      setFormOpen(false);
      refetch();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar la colección");
    } finally {
      setSaving(false);
    }
  };

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
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Colecciones</h2>
        <button className="btn btn-primary" onClick={openCreate}>
          + Nueva Colección
        </button>
      </div>

      {isLoading ? (
        <div style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>
          Cargando...
        </div>
      ) : (data?.items.length ?? 0) === 0 ? (
        <div className="card" style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>
          No hay colecciones creadas todavía.
        </div>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))",
            gap: 16,
          }}
        >
          {data?.items.map((c) => (
            <div key={c.id} className="card" style={{ padding: 16 }}>
              <div
                style={{
                  width: "100%",
                  height: 140,
                  borderRadius: 16,
                  background: c.imagen_url
                    ? `url(${c.imagen_url}) center/cover`
                    : colors.gradientBackground,
                  marginBottom: 12,
                }}
              />
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 4 }}>{c.nombre}</div>
              {c.descripcion && (
                <div style={{ fontSize: 12, color: colors.grayNeutral, marginBottom: 10 }}>
                  {c.descripcion}
                </div>
              )}
              <div style={{ display: "flex", gap: 8 }}>
                <button className="btn btn-secondary" onClick={() => openEdit(c)}>
                  Editar
                </button>
                <button className="btn btn-danger" onClick={() => setDeleting(c)}>
                  Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {formOpen && (
        <div className="modal-overlay">
          <form onSubmit={handleSubmit} className="card modal-card" style={{ maxWidth: 460 }}>
            <h3 style={{ margin: 0, color: colors.purpleDark }}>
              {editing ? "Editar colección" : "Nueva colección"}
            </h3>

            <div>
              <label htmlFor="nombre">Nombre</label>
              <input
                id="nombre"
                value={form.nombre}
                onChange={(e) => setForm({ ...form, nombre: e.target.value })}
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
              <button type="button" className="btn btn-secondary" onClick={() => setFormOpen(false)}>
                Cancelar
              </button>
              <button type="submit" className="btn btn-primary" disabled={saving || uploading}>
                {saving ? "Guardando..." : "Guardar"}
              </button>
            </div>
          </form>
        </div>
      )}

      {deleting && (
        <ConfirmDialog
          open
          title="Eliminar colección"
          message={`¿Seguro que deseas eliminar "${deleting.nombre}"? Esta acción no se puede deshacer.`}
          onCancel={() => setDeleting(null)}
          onConfirm={async () => {
            try {
              await deleteColeccion(deleting.id);
              toast.success("Colección eliminada");
              refetch();
            } catch {
              toast.error("No se pudo eliminar la colección");
            } finally {
              setDeleting(null);
            }
          }}
        />
      )}
    </div>
  );
}
