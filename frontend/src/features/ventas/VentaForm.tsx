import { FormEvent, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { colors } from "../../theme/colors";
import { fetchClientes } from "../clientes/clientesApi";
import { createVenta, type VentaInput } from "./ventasApi";

interface VentaFormProps {
  onClose: () => void;
  onSaved: () => void;
}

const EMPTY: VentaInput = {
  cliente_id: 0,
  total: 0,
  fecha_factura: "",
  fecha_entrega: "",
  tipo_compra: "",
  observaciones: "",
};

export function VentaForm({ onClose, onSaved }: VentaFormProps) {
  const [form, setForm] = useState<VentaInput>(EMPTY);
  const [saving, setSaving] = useState(false);

  const { data: clientesData } = useQuery({
    queryKey: ["clientes-select"],
    queryFn: () => fetchClientes({ page: 1, per_page: 200 }),
  });

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!form.cliente_id) {
      toast.error("Seleccioná un cliente");
      return;
    }
    setSaving(true);
    try {
      await createVenta(form);
      toast.success("Venta creada");
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar la venta");
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
        style={{ width: "100%", maxWidth: 520, display: "flex", flexDirection: "column", gap: 14 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>Nueva venta</h3>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
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
          <div>
            <label htmlFor="total">Total</label>
            <input
              id="total"
              type="number"
              step="0.01"
              min={0}
              value={form.total}
              onChange={(e) => setForm({ ...form, total: Number(e.target.value) })}
              required
            />
          </div>
          <div>
            <label htmlFor="tipo_compra">Tipo de compra</label>
            <input
              id="tipo_compra"
              value={form.tipo_compra ?? ""}
              onChange={(e) => setForm({ ...form, tipo_compra: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="fecha_factura">Fecha de factura</label>
            <input
              id="fecha_factura"
              type="date"
              value={form.fecha_factura ?? ""}
              onChange={(e) => setForm({ ...form, fecha_factura: e.target.value })}
            />
          </div>
          <div>
            <label htmlFor="fecha_entrega">Fecha de entrega</label>
            <input
              id="fecha_entrega"
              type="date"
              value={form.fecha_entrega ?? ""}
              onChange={(e) => setForm({ ...form, fecha_entrega: e.target.value })}
            />
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="observaciones">Observaciones</label>
            <textarea
              id="observaciones"
              rows={2}
              value={form.observaciones ?? ""}
              onChange={(e) => setForm({ ...form, observaciones: e.target.value })}
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
