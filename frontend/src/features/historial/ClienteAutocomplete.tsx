import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import type { Cliente } from "../../api/types";
import { colors } from "../../theme/colors";
import { fetchClientes } from "../clientes/clientesApi";

interface ClienteAutocompleteProps {
  selected: Cliente | null;
  onSelect: (cliente: Cliente | null) => void;
}

export function ClienteAutocomplete({ selected, onSelect }: ClienteAutocompleteProps) {
  const [query, setQuery] = useState(selected?.razon_social ?? "");
  const [open, setOpen] = useState(false);

  const { data } = useQuery({
    queryKey: ["clientes-autocomplete", query],
    queryFn: () => fetchClientes({ q: query, page: 1, per_page: 8 }),
    enabled: query.trim().length > 0 && open,
  });

  const sugerencias = data?.items ?? [];

  return (
    <div style={{ position: "relative", maxWidth: 420 }}>
      <label htmlFor="cliente-autocomplete">Cliente</label>
      <input
        id="cliente-autocomplete"
        placeholder="Buscar por razón social o RUC..."
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
          if (e.target.value.trim() === "") onSelect(null);
        }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
      />
      {open && sugerencias.length > 0 && (
        <div
          className="card"
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            right: 0,
            marginTop: 4,
            padding: 6,
            zIndex: 20,
            maxHeight: 260,
            overflowY: "auto",
          }}
        >
          {sugerencias.map((c) => (
            <div
              key={c.id}
              onMouseDown={() => {
                onSelect(c);
                setQuery(c.razon_social);
                setOpen(false);
              }}
              style={{
                padding: "8px 10px",
                borderRadius: 10,
                cursor: "pointer",
                fontSize: 13,
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = colors.grayLight)}
              onMouseLeave={(e) => (e.currentTarget.style.background = "transparent")}
            >
              <div style={{ fontWeight: 600 }}>{c.razon_social}</div>
              <div style={{ fontSize: 11, color: colors.grayNeutral }}>{c.ruc ?? "-"}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
