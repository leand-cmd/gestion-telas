import { colors } from "../../theme/colors";

interface ColeccionCardProps {
  nombre: string;
  imagenUrl: string | null;
  count: number;
  expanded: boolean;
  onToggle: () => void;
  onEdit?: () => void;
  onImagenClick: () => void;
}

export function ColeccionCard({
  nombre,
  imagenUrl,
  count,
  expanded,
  onToggle,
  onEdit,
  onImagenClick,
}: ColeccionCardProps) {
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
      <div style={{ display: "flex", gap: 8 }}>
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
    </div>
  );
}
