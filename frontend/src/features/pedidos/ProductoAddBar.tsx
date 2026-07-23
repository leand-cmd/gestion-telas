import { useRef, useState } from "react";

import type { Coleccion, Producto } from "../../api/types";
import { colors } from "../../theme/colors";

interface ProductoAddBarProps {
  productos: Producto[];
  coleccionPorId: Map<number, Coleccion>;
  onAdd: (producto: Producto) => void;
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

export function ProductoAddBar({ productos, coleccionPorId, onAdd }: ProductoAddBarProps) {
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

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
        p.categoria.toLowerCase().includes(q) ||
        (p.color_general ?? "").toLowerCase().includes(q) ||
        (p.descripcion ?? "").toLowerCase().includes(q)
    );
    const porCodigo = matches.filter((p) => p.cod_producto.toLowerCase().includes(q));
    const otros = matches.filter((p) => !p.cod_producto.toLowerCase().includes(q));
    return [...porCodigo, ...otros].slice(0, MAX_RESULTADOS);
  })();

  const seleccionar = (p: Producto) => {
    onAdd(p);
    setQuery("");
    setOpen(false);
    inputRef.current?.focus();
  };

  return (
    <div className="card" style={{ padding: 12, border: `1px solid ${colors.purplePrimary}` }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <input
          ref={inputRef}
          value={query}
          placeholder="Buscar producto por código, colección, categoría, color..."
          style={{ fontSize: 16, padding: "14px 16px" }}
          onChange={(e) => {
            setQuery(e.target.value);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
          onBlur={() => setTimeout(() => setOpen(false), 150)}
        />
        <div
          aria-hidden
          style={{
            flexShrink: 0,
            width: 44,
            height: 44,
            borderRadius: 12,
            background: colors.gradientBackground,
            color: colors.white,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 20,
            fontWeight: 700,
          }}
        >
          +
        </div>
      </div>

      {open && resultados.length > 0 && (
        <div style={{ marginTop: 10, maxHeight: 320, overflowY: "auto" }}>
          {resultados.map((p) => (
            <div
              key={p.id}
              onMouseDown={(e) => {
                e.preventDefault();
                seleccionar(p);
              }}
              style={{
                padding: "10px 12px",
                borderRadius: 10,
                cursor: "pointer",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: 8,
                minHeight: 44,
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = "rgba(108,93,209,0.08)")}
              onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
            >
              <div>
                <div style={{ fontWeight: 700, fontSize: 15 }}>{highlight(p.cod_producto, q)}</div>
                <div style={{ fontSize: 12, color: colors.grayNeutral }}>
                  {nombreColeccion(p)} · {p.categoria} · {p.color_general ?? "-"}
                </div>
              </div>
              <div style={{ fontWeight: 600, fontSize: 13, whiteSpace: "nowrap" }}>
                {formatPrecio(p.precio_rollo)}
              </div>
            </div>
          ))}
        </div>
      )}

      {open && q && resultados.length === 0 && (
        <div style={{ marginTop: 10, padding: "8px 12px", fontSize: 13, color: colors.grayNeutral }}>
          Sin resultados para "{query}"
        </div>
      )}
    </div>
  );
}
