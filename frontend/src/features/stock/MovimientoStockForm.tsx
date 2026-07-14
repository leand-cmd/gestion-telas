import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { StockItem, StockMovimientoTipo } from "../../api/types";
import { colors } from "../../theme/colors";
import { crearMovimiento } from "./stockApi";

interface MovimientoStockFormProps {
  producto: StockItem;
  onClose: () => void;
  onSaved: () => void;
}

const TIPOS: StockMovimientoTipo[] = ["entrada", "salida", "ajuste"];

export function MovimientoStockForm({ producto, onClose, onSaved }: MovimientoStockFormProps) {
  const [tipo, setTipo] = useState<StockMovimientoTipo>("entrada");
  const [cantidad, setCantidad] = useState(1);
  const [motivo, setMotivo] = useState("");
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await crearMovimiento({ producto_id: producto.id, tipo, cantidad, motivo: motivo || null });
      toast.success("Movimiento registrado");
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo registrar el movimiento");
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
        style={{ width: "100%", maxWidth: 420, display: "flex", flexDirection: "column", gap: 14 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          Movimiento de stock — {producto.cod_sku}
        </h3>
        <p style={{ margin: 0, fontSize: 13, color: colors.grayNeutral }}>
          Stock actual: {producto.stock_actual}
        </p>

        <div>
          <label htmlFor="tipo">Tipo</label>
          <select id="tipo" value={tipo} onChange={(e) => setTipo(e.target.value as StockMovimientoTipo)}>
            {TIPOS.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="cantidad">Cantidad</label>
          <input
            id="cantidad"
            type="number"
            min={1}
            value={cantidad}
            onChange={(e) => setCantidad(Number(e.target.value))}
            required
          />
        </div>
        <div>
          <label htmlFor="motivo">Motivo</label>
          <input id="motivo" value={motivo} onChange={(e) => setMotivo(e.target.value)} />
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Guardando..." : "Registrar"}
          </button>
        </div>
      </form>
    </div>
  );
}
