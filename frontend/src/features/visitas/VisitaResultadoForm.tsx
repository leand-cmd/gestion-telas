import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { TIPOS_GESTION } from "./visitaOptions";
import { createVisita, registrarResultado } from "./visitasApi";

interface VisitaResultadoFormProps {
  visita: Visita;
  onClose: () => void;
  onSaved: () => void;
}

export function VisitaResultadoForm({ visita, onClose, onSaved }: VisitaResultadoFormProps) {
  const [tipoGestion, setTipoGestion] = useState(visita.tipo_gestion ?? "");
  const [reprogramando, setReprogramando] = useState(false);
  const [fecha, setFecha] = useState("");
  const [hora, setHora] = useState("");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!tipoGestion) {
      toast.error("Seleccioná un tipo de gestión");
      return;
    }
    if (reprogramando && (!fecha || !hora)) {
      toast.error("Completá la fecha y hora de la nueva visita");
      return;
    }

    setSaving(true);
    try {
      await registrarResultado(visita.id, { tipo_gestion: tipoGestion });

      if (reprogramando) {
        await createVisita({
          cliente_id: visita.cliente_id,
          asesor_id: visita.asesor_id,
          fecha,
          hora,
          proposito: visita.proposito,
          notas_previas: `Reprogramada desde la visita del ${visita.fecha} ${visita.hora ?? ""} (${tipoGestion}).`,
        });
      }

      toast.success(reprogramando ? "Gestión registrada y visita reprogramada" : "Gestión registrada");
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar la gestión");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay">
      <form onSubmit={handleSubmit} className="card modal-card" style={{ maxWidth: 440 }}>
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          Gestión — {visita.cliente?.razon_social}
        </h3>

        <div>
          <label htmlFor="tipo_gestion">Tipo de gestión</label>
          <select
            id="tipo_gestion"
            value={tipoGestion}
            onChange={(e) => setTipoGestion(e.target.value)}
            required
          >
            <option value="">Seleccionar...</option>
            {TIPOS_GESTION.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        {reprogramando && (
          <div className="form-grid">
            <div>
              <label htmlFor="fecha">Nueva fecha</label>
              <input
                id="fecha"
                type="date"
                value={fecha}
                onChange={(e) => setFecha(e.target.value)}
                required
              />
            </div>
            <div>
              <label htmlFor="hora">Nueva hora</label>
              <input
                id="hora"
                type="time"
                value={hora}
                onChange={(e) => setHora(e.target.value)}
                required
              />
            </div>
          </div>
        )}

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8, flexWrap: "wrap" }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => setReprogramando((r) => !r)}
          >
            {reprogramando ? "No reprogramar" : "📅 Reprogramar Visita"}
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Guardando..." : reprogramando ? "Guardar" : "Guardar Gestión"}
          </button>
        </div>
      </form>
    </div>
  );
}
