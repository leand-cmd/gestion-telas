import { FormEvent, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import toast from "react-hot-toast";

import type { Pedido } from "../../api/types";
import { colors } from "../../theme/colors";
import { fetchClientes } from "../clientes/clientesApi";
import { fetchProductos } from "../productos/productosApi";
import { createPedido, updatePedido, type PedidoDetalleInput, type PedidoInput } from "./pedidosApi";

interface PedidoFormProps {
  pedido: Pedido | null;
  onClose: () => void;
  onSaved: () => void;
}

interface LineaForm extends PedidoDetalleInput {
  key: string;
}

function lineaVacia(): LineaForm {
  return { key: crypto.randomUUID(), producto_id: 0, cantidad: 1, valor_unitario: null };
}

export function PedidoForm({ pedido, onClose, onSaved }: PedidoFormProps) {
  const [clienteId, setClienteId] = useState<number>(pedido?.cliente_id ?? 0);
  const [tipoCompra, setTipoCompra] = useState(pedido?.tipo_compra ?? "");
  const [fechaPedido, setFechaPedido] = useState(pedido?.fecha_pedido ?? "");
  const [fechaEntrega, setFechaEntrega] = useState(pedido?.fecha_entrega_estimada ?? "");
  const [observaciones, setObservaciones] = useState(pedido?.observaciones ?? "");
  const [lineas, setLineas] = useState<LineaForm[]>(
    pedido?.detalles?.length
      ? pedido.detalles.map((d) => ({
          key: crypto.randomUUID(),
          producto_id: d.producto_id,
          cantidad: d.cantidad,
          valor_unitario: d.valor_unitario,
        }))
      : [lineaVacia()]
  );
  const [saving, setSaving] = useState(false);

  const { data: clientesData } = useQuery({
    queryKey: ["clientes-select"],
    queryFn: () => fetchClientes({ page: 1, per_page: 200 }),
  });
  const { data: productosData } = useQuery({
    queryKey: ["productos-select"],
    queryFn: () => fetchProductos({ page: 1, per_page: 200 }),
  });

  const productos = productosData?.items ?? [];

  const total = useMemo(() => {
    return lineas.reduce((acc, l) => {
      const producto = productos.find((p) => p.id === l.producto_id);
      const valor = l.valor_unitario ?? producto?.precio ?? 0;
      return acc + valor * l.cantidad;
    }, 0);
  }, [lineas, productos]);

  const actualizarLinea = (key: string, cambios: Partial<LineaForm>) => {
    setLineas((prev) => prev.map((l) => (l.key === key ? { ...l, ...cambios } : l)));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!clienteId) {
      toast.error("Seleccioná un cliente");
      return;
    }
    const detalles = lineas
      .filter((l) => l.producto_id > 0 && l.cantidad > 0)
      .map(({ producto_id, cantidad, valor_unitario }) => ({ producto_id, cantidad, valor_unitario }));

    if (detalles.length === 0) {
      toast.error("Agregá al menos un producto");
      return;
    }

    const input: PedidoInput = {
      cliente_id: clienteId,
      tipo_compra: tipoCompra || null,
      fecha_pedido: fechaPedido || null,
      fecha_entrega_estimada: fechaEntrega || null,
      observaciones: observaciones || null,
      detalles,
    };

    setSaving(true);
    try {
      if (pedido) {
        await updatePedido(pedido.id, input);
        toast.success("Pedido actualizado");
      } else {
        await createPedido(input);
        toast.success("Pedido creado");
      }
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar el pedido");
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
        style={{ width: "100%", maxWidth: 760, display: "flex", flexDirection: "column", gap: 14 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          {pedido ? `Editar pedido ${pedido.nro_pedido}` : "Nuevo pedido"}
        </h3>

        <div className="form-grid">
          <div>
            <label htmlFor="cliente_id">Cliente</label>
            <select
              id="cliente_id"
              value={clienteId}
              onChange={(e) => setClienteId(Number(e.target.value))}
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
            <label htmlFor="tipo_compra">Tipo de compra</label>
            <input
              id="tipo_compra"
              value={tipoCompra ?? ""}
              onChange={(e) => setTipoCompra(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="fecha_pedido">Fecha del pedido</label>
            <input
              id="fecha_pedido"
              type="date"
              value={fechaPedido ?? ""}
              onChange={(e) => setFechaPedido(e.target.value)}
            />
          </div>
          <div>
            <label htmlFor="fecha_entrega_estimada">Entrega estimada</label>
            <input
              id="fecha_entrega_estimada"
              type="date"
              value={fechaEntrega ?? ""}
              onChange={(e) => setFechaEntrega(e.target.value)}
            />
          </div>
          <div style={{ gridColumn: "1 / -1" }}>
            <label htmlFor="observaciones">Observaciones</label>
            <textarea
              id="observaciones"
              rows={2}
              value={observaciones ?? ""}
              onChange={(e) => setObservaciones(e.target.value)}
            />
          </div>
        </div>

        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <label>Detalle del pedido</label>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setLineas((prev) => [...prev, lineaVacia()])}
            >
              + Agregar producto
            </button>
          </div>

          <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>Producto</th>
                <th>Cantidad</th>
                <th>Valor unitario</th>
                <th>Subtotal</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {lineas.map((l) => {
                const producto = productos.find((p) => p.id === l.producto_id);
                const valor = l.valor_unitario ?? producto?.precio ?? 0;
                return (
                  <tr key={l.key}>
                    <td>
                      <select
                        value={l.producto_id}
                        onChange={(e) =>
                          actualizarLinea(l.key, { producto_id: Number(e.target.value) })
                        }
                      >
                        <option value={0}>Seleccionar...</option>
                        {productos.map((p) => (
                          <option key={p.id} value={p.id}>
                            {p.cod_sku} - {p.descripcion ?? ""}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td>
                      <input
                        type="number"
                        min={1}
                        style={{ width: 80 }}
                        value={l.cantidad}
                        onChange={(e) =>
                          actualizarLinea(l.key, { cantidad: Number(e.target.value) })
                        }
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        step="0.01"
                        style={{ width: 110 }}
                        value={valor}
                        onChange={(e) =>
                          actualizarLinea(l.key, { valor_unitario: Number(e.target.value) })
                        }
                      />
                    </td>
                    <td>₲ {(valor * l.cantidad).toLocaleString("es-PY")}</td>
                    <td>
                      <button
                        type="button"
                        className="btn btn-danger"
                        disabled={lineas.length === 1}
                        onClick={() =>
                          setLineas((prev) => prev.filter((x) => x.key !== l.key))
                        }
                      >
                        Quitar
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          </div>

          <div style={{ textAlign: "right", fontWeight: 700, marginTop: 8, color: colors.purpleDark }}>
            Total: ₲ {total.toLocaleString("es-PY")}
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
