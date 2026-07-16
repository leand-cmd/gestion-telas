import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { createVisita } from "./visitasApi";

interface ReagendarVisitaFormProps {
  visita: Visita;
  onClose: () => void;
  onSaved: () => void;
}

export function ReagendarVisitaForm({ visita, onClose, onSaved }: ReagendarVisitaFormProps) {
  const [fecha, setFecha] = useState("");
  const [hora, setHora] = useState("");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await createVisita({
        cliente_id: visita.cliente_id,
        asesor_id: visita.asesor_id,
        fecha,
        hora,
        proposito: visita.proposito,
        direccion: visita.direccion,
        notas_previas: `Reagendada desde la visita del ${visita.fecha} ${visita.hora} (${visita.tipo_gestion}).`,
      });
      toast.success("Visita reagendada");
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo reagendar la visita");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay">
      <form onSubmit={handleSubmit} className="card modal-card" style={{ maxWidth: 420 }}>
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          Reagendar visita — {visita.cliente?.razon_social}
        </h3>
        <p style={{ margin: 0, fontSize: 13, color: colors.grayNeutral }}>
          Se creará una nueva visita programada. La visita original ({visita.fecha} {visita.hora})
          queda como referencia en el historial.
        </p>

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

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Guardando..." : "Reagendar"}
          </button>
        </div>
      </form>
    </div>
  );
}
