import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import { Column, DataTable } from "../../components/DataTable";
import { Pagination } from "../../components/Pagination";
import type { StockItem } from "../../api/types";
import { colors } from "../../theme/colors";
import { MovimientoStockForm } from "./MovimientoStockForm";
import { fetchStock } from "./stockApi";

export function StockList() {
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const [soloBajoMinimo, setSoloBajoMinimo] = useState(false);
  const [registrando, setRegistrando] = useState<StockItem | null>(null);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["stock", { page, q, soloBajoMinimo }],
    queryFn: () => fetchStock({ page, per_page: 10, q, bajo_minimo: soloBajoMinimo || undefined }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["stock"] });

  const columns: Column<StockItem>[] = [
    { header: "Cod Producto", render: (p) => p.cod_producto },
    { header: "Descripción", render: (p) => p.descripcion_completa ?? "-", truncate: true },
    { header: "Stock actual", render: (p) => p.stock_actual },
    { header: "Stock mínimo", render: (p) => p.stock_minimo ?? "-" },
    {
      header: "Estado",
      render: (p) => (
        <span className={`badge ${p.bajo_minimo ? "badge-inactive" : "badge-active"}`}>
          {p.bajo_minimo ? "Bajo mínimo" : "OK"}
        </span>
      ),
    },
    {
      header: "Acciones",
      render: (p) => (
        <button className="btn btn-primary" onClick={() => setRegistrando(p)}>
          Registrar movimiento
        </button>
      ),
    },
  ];

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Stock</h2>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
          <input
            placeholder="Buscar por SKU o descripción..."
            value={q}
            onChange={(e) => {
              setQ(e.target.value);
              setPage(1);
            }}
            style={{ width: 260 }}
          />
          <label style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 13 }}>
            <input
              type="checkbox"
              checked={soloBajoMinimo}
              onChange={(e) => {
                setSoloBajoMinimo(e.target.checked);
                setPage(1);
              }}
            />
            Solo bajo mínimo
          </label>
        </div>
      </div>

      <div className="card">
        <DataTable
          columns={columns}
          rows={data?.items ?? []}
          rowKey={(p) => p.id}
          loading={isLoading}
          emptyMessage="No se encontraron productos"
        />
        {data && (
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        )}
      </div>

      {registrando && (
        <MovimientoStockForm
          producto={registrando}
          onClose={() => setRegistrando(null)}
          onSaved={() => {
            setRegistrando(null);
            refetch();
          }}
        />
      )}
    </div>
  );
}
