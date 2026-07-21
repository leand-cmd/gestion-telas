import type { Producto } from "../../api/types";
import { colors } from "../../theme/colors";

interface ProductDetailModalProps {
  producto: Producto;
  onClose: () => void;
}

function Campo({ label, value }: { label: string; value: string | number | null | undefined }) {
  if (value == null || value === "") return null;
  return (
    <div>
      <div style={{ fontSize: 11, fontWeight: 700, color: colors.grayNeutral, textTransform: "uppercase" }}>
        {label}
      </div>
      <div style={{ fontSize: 14 }}>{value}</div>
    </div>
  );
}

export function ProductDetailModal({ producto: p, onClose }: ProductDetailModalProps) {
  const formatPrecio = (v: number | null) => (v != null ? `₲ ${v.toLocaleString("es-PY")}` : null);

  return (
    <div className="modal-overlay">
      <div className="card modal-card" style={{ maxWidth: 560, position: "relative" }}>
        <button
          type="button"
          className="btn btn-secondary"
          onClick={onClose}
          style={{
            position: "absolute",
            top: 12,
            right: 12,
            padding: "4px 10px",
            fontSize: 14,
            lineHeight: 1,
          }}
          title="Cerrar"
        >
          ✕
        </button>

        <div style={{ paddingRight: 32 }}>
          <h3 style={{ margin: 0, color: colors.purpleDark }}>{p.cod_producto}</h3>
        </div>

        {p.imagen_url && (
          <img
            src={p.imagen_url}
            alt={p.cod_producto}
            style={{ width: "100%", maxHeight: 260, objectFit: "cover", borderRadius: 16 }}
          />
        )}

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
          <Campo label="Proveedor" value={p.proveedor} />
          <Campo label="Marca" value={p.marca} />
          <Campo label="Categoría" value={p.categoria} />
          <Campo label="Sub Categoría" value={p.sub_categoria} />
          <Campo label="Tipo Diseño" value={p.tipo_diseno} />
          <Campo label="Cod Color" value={p.cod_color} />
          <Campo label="Color General" value={p.color_general} />
          <Campo label="Color Inferido" value={p.color_descripcion} />
          <Campo label="Composición" value={p.composicion} />
          <Campo label="Línea Sugerida" value={p.linea_sugerida} />
          <Campo label="Ancho" value={p.ancho_cm != null ? `${p.ancho_cm} cm` : null} />
          <Campo label="Gramaje" value={p.gramaje_gm2 != null ? `${p.gramaje_gm2} g/m²` : null} />
          <Campo label="Precio Rollo" value={formatPrecio(p.precio_rollo)} />
          <Campo label="Precio 1/2 Rollo" value={formatPrecio(p.precio_media_rollo)} />
          <Campo label="Precio Corte" value={formatPrecio(p.precio_corte)} />
          <Campo label="Stock" value={p.stock_rollos != null ? `${p.stock_rollos} rollos` : null} />
          <div style={{ gridColumn: "1 / -1" }}>
            <Campo label="Descripción" value={p.descripcion} />
          </div>
        </div>

        <div className="modal-actions">
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}
