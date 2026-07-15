import { FormEvent, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { colors } from "../../theme/colors";
import { fetchClientes } from "../clientes/clientesApi";
import { fetchAsesores } from "../usuarios/usuariosApi";
import { PROPOSITOS } from "./visitaOptions";
import { createVisita, type VisitaInput } from "./visitasApi";

interface VisitaFormProps {
  onClose: () => void;
  onSaved: () => void;
}

const EMPTY: VisitaInput = {
  cliente_id: 0,
  asesor_id: 0,
  fecha: "",
  hora: "",
  proposito: "",
  direccion: "",
  notas_previas: "",
};

export function VisitaForm({ onClose, onSaved }: VisitaFormProps) {
  const [form, setForm] = useState<VisitaInput>(EMPTY);
  const [saving, setSaving] = useState(false);

  const { data: clientesData } = useQuery({
    queryKey: ["clientes-select"],
    queryFn: () => fetchClientes({ page: 1, per_page: 200 }),
  });
  const { data: asesores } = useQuery({ queryKey: ["asesores"], queryFn: fetchAsesores });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.cliente_id || !form.asesor_id) {
      toast.error("Seleccioná cliente y asesor");
      return;
    }
    setSaving(true);
    try {
      await createVisita({ ...form, proposito: form.proposito || null });
      toast.success("Visita programada");
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo programar la visita");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="modal-overlay">
      <form onSubmit={handleSubmit} className="card modal-card" style={{ maxWidth: 520 }}>
        <h3 style={{ margin: 0, color: colors.purpleDark }}>Programar visita</h3>

        <div className="form-grid">
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="cliente_id">Cliente</label>
            <select
              id="cliente_id"
              value={form.cliente_id}
              onChange={(e) => setForm({ ...form, cliente_id: Number(e.target.value) })}
              required
            >
              <option value={0}>Seleccionar...</option>
              {(clientesData?.items ?? []).map((c) => (
                <option key={c.id} value={c.id}>
                  {c.razon_social}
                </option>
              ))}
            </select>
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="asesor_id">Asesor</label>
            <select
              id="asesor_id"
              value={form.asesor_id}
              onChange={(e) => setForm({ ...form, asesor_id: Number(e.target.value) })}
              required
            >
              <option value={0}>Seleccionar...</option>
              {(asesores ?? []).map((a) => (
                <option key={a.id} value={a.id}>
                  {a.nombre}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="fecha">Fecha</label>
            <input
              id="fecha"
              type="date"
              value={form.fecha}
              onChange={(e) => setForm({ ...form, fecha: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="hora">Hora</label>
            <input
              id="hora"
              type="time"
              value={form.hora}
              onChange={(e) => setForm({ ...form, hora: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="proposito">Propósito</label>
            <select
              id="proposito"
              value={form.proposito ?? ""}
              onChange={(e) => setForm({ ...form, proposito: e.target.value })}
            >
              <option value="">Seleccionar...</option>
              {PROPOSITOS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="direccion">Dirección</label>
            <input
              id="direccion"
              value={form.direccion ?? ""}
              onChange={(e) => setForm({ ...form, direccion: e.target.value })}
            />
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="notas_previas">Notas previas</label>
            <textarea
              id="notas_previas"
              rows={2}
              value={form.notas_previas ?? ""}
              onChange={(e) => setForm({ ...form, notas_previas: e.target.value })}
            />
          </div>
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
