import { useState } from "react";
import toast from "react-hot-toast";

import { ConfirmDialog } from "../../components/ConfirmDialog";
import { colors } from "../../theme/colors";
import { deleteColeccion } from "../colecciones/coleccionesApi";

interface ColeccionCardProps {
  coleccionId: number | null;
  nombre: string;
  imagenUrl: string | null;
  count: number;
  expanded: boolean;
  onToggle: () => void;
  onEdit?: () => void;
  onImagenClick: () => void;
  onDeleted?: () => void;
}

export function ColeccionCard({
  coleccionId,
  nombre,
  imagenUrl,
  count,
  expanded,
  onToggle,
  onEdit,
  onImagenClick,
  onDeleted,
}: ColeccionCardProps) {
  const [confirmingDelete, setConfirmingDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleEliminar = async () => {
    if (coleccionId == null) return;
    setDeleting(true);
    try {
      await deleteColeccion(coleccionId);
      toast.success("Colección eliminada");
      onDeleted?.();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo eliminar la colección");
    } finally {
      setDeleting(false);
      setConfirmingDelete(false);
    }
  };

  return (
    <div
      className="card coleccion-card"
      style={{ border: expanded ? `2px solid ${colors.purplePrimary}` : undefined }}
      onClick={onToggle}
    >
      <div
        className="coleccion-card-imagen"
        style={{
          background: imagenUrl ? `url(${imagenUrl}) center/cover` : colors.gradientBackground,
        }}
        onClick={(e) => {
          if (!imagenUrl) return;
          e.stopPropagation();
          onImagenClick();
        }}
      />
      <div style={{ fontWeight: 700, fontSize: 15 }}>{nombre}</div>
      <div style={{ fontSize: 12, color: colors.grayNeutral, marginBottom: 8 }}>
        {count} {count === 1 ? "producto" : "productos"}
      </div>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {imagenUrl && (
          <button
            className="btn btn-secondary"
            style={{ padding: "4px 10px", fontSize: 13 }}
            onClick={(e) => {
              e.stopPropagation();
              onImagenClick();
            }}
            title="Ver imagen completa"
          >
            🔍
          </button>
        )}
        {onEdit && (
          <button
            className="btn btn-secondary"
            style={{ padding: "4px 10px", fontSize: 13 }}
            onClick={(e) => {
              e.stopPropagation();
              onEdit();
            }}
            title="Editar colección"
          >
            ✎
          </button>
        )}
        {coleccionId != null && (
          <button
            className="btn btn-secondary"
            style={{ padding: "4px 10px", fontSize: 13 }}
            onClick={(e) => {
              e.stopPropagation();
              setConfirmingDelete(true);
            }}
            title="Eliminar colección"
          >
            🗑️
          </button>
        )}
        <button
          className="btn btn-secondary"
          style={{ padding: "4px 10px", fontSize: 13, marginLeft: "auto" }}
          onClick={(e) => {
            e.stopPropagation();
            onToggle();
          }}
          title={expanded ? "Colapsar" : "Expandir"}
        >
          {expanded ? "−" : "+"}
        </button>
      </div>

      {confirmingDelete && (
        <div onClick={(e) => e.stopPropagation()}>
          <ConfirmDialog
            open
            title="Eliminar colección"
            message={`¿Eliminar la colección "${nombre}"? Los productos que contiene pasarán a "Sin colección".`}
            confirmLabel={deleting ? "Eliminando..." : "Eliminar"}
            onCancel={() => setConfirmingDelete(false)}
            onConfirm={handleEliminar}
          />
        </div>
      )}
    </div>
  );
}
