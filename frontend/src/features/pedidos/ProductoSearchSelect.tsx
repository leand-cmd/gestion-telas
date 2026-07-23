import { useState } from "react";

import type { Coleccion, Producto } from "../../api/types";
import { colors } from "../../theme/colors";

interface ProductoSearchSelectProps {
  productos: Producto[];
  coleccionPorId: Map<number, Coleccion>;
  value: number;
  onChange: (id: number) => void;
}

const MAX_RESULTADOS = 10;

function highlight(text: string, query: string) {
  const idx = text.toLowerCase().indexOf(query.toLowerCase());
  if (idx === -1) return text;
  return (
    <>
      {text.slice(0, idx)}
      <mark style={{ background: colors.pinkLight, color: "inherit", borderRadius: 3, padding: "0 2px" }}>
        {text.slice(idx, idx + query.length)}
      </mark>
      {text.slice(idx + query.length)}
    </>
  );
}

export function ProductoSearchSelect({
  productos,
  coleccionPorId,
  value,
  onChange,
}: ProductoSearchSelectProps) {
  const seleccionado = productos.find((p) => p.id === value) ?? null;
  const [query, setQuery] = useState(seleccionado?.cod_producto ?? "");
  const [open, setOpen] = useState(false);

  const formatPrecio = (v: number | null) => (v != null ? `₲ ${v.toLocaleString("es-PY")}` : "-");
  const nombreColeccion = (p: Producto) =>
    (p.coleccion_id != null ? coleccionPorId.get(p.coleccion_id)?.nombre : null) ?? "Sin colección";

  const q = query.trim().toLowerCase();
  const resultados = (() => {
    if (!q) return [];
    const matches = productos.filter(
      (p) =>
        p.cod_producto.toLowerCase().includes(q) ||
        nombreColeccion(p).toLowerCase().includes(q) ||
        (p.color_general ?? "").toLowerCase().includes(q) ||
        (p.descripcion ?? "").toLowerCase().includes(q)
    );
    const porCodigo = matches.filter((p) => p.cod_producto.toLowerCase().includes(q));
    const otros = matches.filter((p) => !p.cod_producto.toLowerCase().includes(q));
    return [...porCodigo, ...otros].slice(0, MAX_RESULTADOS);
  })();

  const seleccionar = (p: Producto) => {
    onChange(p.id);
    setQuery(p.cod_producto);
    setOpen(false);
  };

  return (
    <div>
      <input
        value={query}
        placeholder="Cod producto, colección, color..."
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
          if (e.target.value.trim() === "") onChange(0);
        }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
      />

      {open && resultados.length > 0 && (
        <div
          className="card"
          style={{ marginTop: 6, padding: 6, maxHeight: 280, overflowY: "auto" }}
        >
          {resultados.map((p) => (
            <div
              key={p.id}
              onMouseDown={(e) => {
                e.preventDefault();
                seleccionar(p);
              }}
              style={{
                padding: "8px 10px",
                borderRadius: 10,
                cursor: "pointer",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: 8,
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(108,93,209,0.08)")}
              onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
            >
              <div>
                <div style={{ fontWeight: 700, fontSize: 15 }}>{highlight(p.cod_producto, q)}</div>
                <div style={{ fontSize: 12, color: colors.grayNeutral }}>
                  {nombreColeccion(p)} · {p.color_general ?? "-"}
                </div>
              </div>
              <div style={{ fontWeight: 600, fontSize: 13, whiteSpace: "nowrap" }}>
                {formatPrecio(p.precio_rollo)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
