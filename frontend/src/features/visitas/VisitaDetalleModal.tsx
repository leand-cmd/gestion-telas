import toast from "react-hot-toast";

import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { colorParaEstadoVisita, labelParaEstadoVisita } from "./visitaEstadoColors";
import { TIPOS_GESTION_REAGENDABLES } from "./visitaOptions";
import { cancelarVisita } from "./visitasApi";

interface VisitaDetalleModalProps {
  visita: Visita;
  onClose: () => void;
  onChanged: () => void;
  onRegistrarResultado: (visita: Visita) => void;
  onReagendar: (visita: Visita) => void;
}

function Campo({ label, value }: { label: string; value: string | null | undefined }) {
  if (!value) return null;
  return (
    <div>
      <div style={{ fontSize: 11, fontWeight: 700, color: colors.grayNeutral, textTransform: "uppercase" }}>
        {label}
      </div>
      <div style={{ fontSize: 14 }}>{value}</div>
    </div>
  );
}

export function VisitaDetalleModal({
  visita,
  onClose,
  onChanged,
  onRegistrarResultado,
  onReagendar,
}: VisitaDetalleModalProps) {
  const c = colorParaEstadoVisita(visita.estado);
  const esReagendable =
    visita.tipo_gestion != null &&
    (TIPOS_GESTION_REAGENDABLES as readonly string[]).includes(visita.tipo_gestion);

  const handleCancelar = async () => {
    try {
      await cancelarVisita(visita.id);
      toast.success("Visita cancelada");
      onChanged();
      onClose();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo cancelar la visita");
    }
  };

  return (
    <div className="modal-overlay">
      <div className="card modal-card" style={{ maxWidth: 460 }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <h3 style={{ margin: 0, color: colors.purpleDark }}>{visita.cliente?.razon_social}</h3>
          <span
            className="badge"
            style={{ background: c.bg, color: c.text, flexShrink: 0 }}
          >
            {labelParaEstadoVisita(visita.estado)}
          </span>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
          <Campo label="Fecha" value={visita.fecha} />
          <Campo label="Hora" value={visita.hora} />
          <Campo label="Asesor" value={visita.asesor?.nombre} />
          <Campo label="Propósito" value={visita.proposito} />
          <div style={{ gridColumn: "1 / -1" }}>
            <Campo label="Dirección" value={visita.direccion} />
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <Campo label="Notas previas" value={visita.notas_previas} />
          </div>
          {visita.estado === "realizada" && (
            <>
              <Campo label="Resultado" value={visita.resultado} />
              <Campo label="Tipo de gestión" value={visita.tipo_gestion} />
              <Campo
                label="Duración"
                value={visita.duracion_actual != null ? `${visita.duracion_actual} min` : null}
              />
              <div style={{ gridColumn: "1 / -1" }}>
                <Campo label="Productos presentados" value={visita.productos_presentados} />
              </div>
              <div style={{ gridColumn: "1 / -1" }}>
                <Campo label="Notas de la visita" value={visita.notas_visita} />
              </div>
              <div style={{ gridColumn: "1 / -1" }}>
                <Campo label="Próxima acción" value={visita.proxima_accion} />
              </div>
            </>
          )}
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8, flexWrap: "wrap" }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cerrar
          </button>
          {esReagendable && (
            <button type="button" className="btn btn-primary" onClick={() => onReagendar(visita)}>
              📅 Reagendar visita
            </button>
          )}
          {visita.estado === "programada" && (
            <>
              <button type="button" className="btn btn-danger" onClick={handleCancelar}>
                Cancelar visita
              </button>
              <button
                type="button"
                className="btn btn-primary"
                onClick={() => onRegistrarResultado(visita)}
              >
                Registrar resultado
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
