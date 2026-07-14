import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Visita } from "../../api/types";
import { colors } from "../../theme/colors";
import { RESULTADOS } from "./visitaOptions";
import { registrarResultado, type VisitaResultadoInput } from "./visitasApi";

interface VisitaResultadoFormProps {
  visita: Visita;
  onClose: () => void;
  onSaved: () => void;
}

export function VisitaResultadoForm({ visita, onClose, onSaved }: VisitaResultadoFormProps) {
  const [form, setForm] = useState<VisitaResultadoInput>({
    resultado: RESULTADOS[0],
    duracion_actual: null,
    presente_cliente: true,
    productos_presentados: "",
    notas_visita: "",
    proxima_accion: "",
  });
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await registrarResultado(visita.id, form);
      toast.success("Resultado registrado");
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo registrar el resultado");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(43,43,56,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        padding: 24,
      }}
    >
      <form
        onSubmit={handleSubmit}
        className="card"
        style={{ width: "100%", maxWidth: 480, display: "flex", flexDirection: "column", gap: 14 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          Resultado de visita — {visita.cliente?.razon_social}
        </h3>

        <div>
          <label htmlFor="resultado">Resultado</label>
          <select
            id="resultado"
            value={form.resultado}
            onChange={(e) => setForm({ ...form, resultado: e.target.value })}
          >
            {RESULTADOS.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="duracion_actual">Duración (minutos)</label>
          <input
            id="duracion_actual"
            type="number"
            min={0}
            value={form.duracion_actual ?? ""}
            onChange={(e) =>
              setForm({ ...form, duracion_actual: e.target.value ? Number(e.target.value) : null })
            }
          />
        </div>
        <div>
          <label htmlFor="presente_cliente">¿El cliente estuvo presente?</label>
          <select
            id="presente_cliente"
            value={form.presente_cliente ? "true" : "false"}
            onChange={(e) => setForm({ ...form, presente_cliente: e.target.value === "true" })}
          >
            <option value="true">Sí</option>
            <option value="false">No</option>
          </select>
        </div>
        <div>
          <label htmlFor="productos_presentados">Productos presentados</label>
          <textarea
            id="productos_presentados"
            rows={2}
            value={form.productos_presentados ?? ""}
            onChange={(e) => setForm({ ...form, productos_presentados: e.target.value })}
          />
        </div>
        <div>
          <label htmlFor="notas_visita">Notas de la visita</label>
          <textarea
            id="notas_visita"
            rows={2}
            value={form.notas_visita ?? ""}
            onChange={(e) => setForm({ ...form, notas_visita: e.target.value })}
          />
        </div>
        <div>
          <label htmlFor="proxima_accion">Próxima acción</label>
          <input
            id="proxima_accion"
            value={form.proxima_accion ?? ""}
            onChange={(e) => setForm({ ...form, proxima_accion: e.target.value })}
          />
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Guardando..." : "Guardar"}
          </button>
        </div>
      </form>
    </div>
  );
}
