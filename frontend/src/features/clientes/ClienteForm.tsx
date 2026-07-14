import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Cliente } from "../../api/types";
import { colors } from "../../theme/colors";
import { CANALES, SUB_CANALES_POR_CANAL, TIPOS_COMPRA } from "./canalOptions";
import { createCliente, updateCliente, type ClienteInput } from "./clientesApi";
import { MapPicker } from "./MapPicker";

interface ClienteFormProps {
  cliente: Cliente | null;
  onClose: () => void;
  onSaved: () => void;
}

const EMPTY: ClienteInput = {
  ruc: "",
  razon_social: "",
  localidad: "",
  barrio: "",
  direccion: "",
  telefono: "",
  email: "",
  canal: "",
  sub_canal: "",
  tipo_compra: "",
  latitude: null,
  longitude: null,
  lista_precios_id: null,
  estado: true,
};

export function ClienteForm({ cliente, onClose, onSaved }: ClienteFormProps) {
  const [form, setForm] = useState<ClienteInput>(cliente ? { ...EMPTY, ...cliente } : EMPTY);
  const [saving, setSaving] = useState(false);

  const subCanalOptions = form.canal ? SUB_CANALES_POR_CANAL[form.canal] ?? [] : [];

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (cliente) {
        await updateCliente(cliente.id, form);
        toast.success("Cliente actualizado");
      } else {
        await createCliente(form);
        toast.success("Cliente creado");
      }
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar el cliente");
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
        overflowY: "auto",
        padding: 24,
      }}
    >
      <form
        onSubmit={handleSubmit}
        className="card"
        style={{ width: "100%", maxWidth: 640, display: "flex", flexDirection: "column", gap: 14 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          {cliente ? "Editar cliente" : "Nuevo cliente"}
        </h3>

        <div className="form-grid">
          <div>
            <label htmlFor="ruc">RUC</label>
            <input
              id="ruc"
              value={form.ruc}
              onChange={(e) => setForm({ ...form, ruc: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="razon_social">Razón Social</label>
            <input
              id="razon_social"
              value={form.razon_social}
              onChange={(e) => setForm({ ...form, razon_social: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="localidad">Localidad</label>
            <input
              id="localidad"
              value={form.localidad ?? ""}
              onChange={(e) => setForm({ ...form, localidad: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="barrio">Barrio</label>
            <input
              id="barrio"
              value={form.barrio ?? ""}
              onChange={(e) => setForm({ ...form, barrio: e.target.value })}
            />
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="direccion">Dirección</label>
            <input
              id="direccion"
              value={form.direccion ?? ""}
              onChange={(e) => setForm({ ...form, direccion: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="telefono">Teléfono</label>
            <input
              id="telefono"
              value={form.telefono ?? ""}
              onChange={(e) => setForm({ ...form, telefono: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={form.email ?? ""}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="canal">Canal</label>
            <select
              id="canal"
              value={form.canal ?? ""}
              onChange={(e) => setForm({ ...form, canal: e.target.value, sub_canal: "" })}
            >
              <option value="">Seleccionar...</option>
              {CANALES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="sub_canal">Sub Canal</label>
            <select
              id="sub_canal"
              value={form.sub_canal ?? ""}
              onChange={(e) => setForm({ ...form, sub_canal: e.target.value })}
              disabled={!form.canal}
            >
              <option value="">Seleccionar...</option>
              {subCanalOptions.map((sc) => (
                <option key={sc} value={sc}>
                  {sc}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="tipo_compra">Tipo Compra</label>
            <select
              id="tipo_compra"
              value={form.tipo_compra ?? ""}
              onChange={(e) => setForm({ ...form, tipo_compra: e.target.value })}
            >
              <option value="">Seleccionar...</option>
              {TIPOS_COMPRA.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="estado">Estado</label>
            <select
              id="estado"
              value={form.estado ? "true" : "false"}
              onChange={(e) => setForm({ ...form, estado: e.target.value === "true" })}
            >
              <option value="true">Activo</option>
              <option value="false">Inactivo</option>
            </select>
          </div>
        </div>

        <MapPicker
          latitude={form.latitude}
          longitude={form.longitude}
          onChange={(lat, lng) => setForm({ ...form, latitude: lat, longitude: lng })}
        />

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
