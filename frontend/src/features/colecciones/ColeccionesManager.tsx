import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { ConfirmDialog } from "../../components/ConfirmDialog";
import type { Coleccion } from "../../api/types";
import { colors } from "../../theme/colors";
import { ColeccionForm } from "./ColeccionForm";
import { deleteColeccion, fetchColecciones } from "./coleccionesApi";

export function ColeccionesManager() {
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Coleccion | null>(null);
  const [deleting, setDeleting] = useState<Coleccion | null>(null);
  const [imagenExpandida, setImagenExpandida] = useState<string | null>(null);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["colecciones"],
    queryFn: fetchColecciones,
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["colecciones"] });

  const openCreate = () => {
    setEditing(null);
    setFormOpen(true);
  };

  const openEdit = (c: Coleccion) => {
    setEditing(c);
    setFormOpen(true);
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
        <div className="colecciones-grid">
          {data?.items.map((c) => (
            <div key={c.id} className="card coleccion-card">
              <div
                className="coleccion-card-imagen"
                style={{
                  background: c.imagen_url
                    ? `url(${c.imagen_url}) center/cover`
                    : colors.gradientBackground,
                }}
                onClick={() => c.imagen_url && setImagenExpandida(c.imagen_url)}
              />
              <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 4 }}>{c.nombre}</div>
              {c.descripcion && (
                <div style={{ fontSize: 12, color: colors.grayNeutral, marginBottom: 10 }}>
                  {c.descripcion}
                </div>
              )}
              <div style={{ display: "flex", gap: 8 }}>
                <button className="btn btn-secondary" onClick={() => openEdit(c)}>
                  ✎ Editar
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
        <ColeccionForm
          coleccion={editing}
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

      {imagenExpandida && (
        <div className="lightbox-overlay" onClick={() => setImagenExpandida(null)}>
          <img src={imagenExpandida} alt="Imagen completa" className="lightbox-imagen" />
        </div>
      )}
    </div>
  );
}
