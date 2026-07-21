import { useQuery } from "@tanstack/react-query";

import { colors } from "../../theme/colors";
import { fetchPedido } from "../pedidos/pedidosApi";

interface ProductosExpandiblesProps {
  pedidoId: number | null;
}

export function ProductosExpandibles({ pedidoId }: ProductosExpandiblesProps) {
  const { data: pedido, isLoading } = useQuery({
    queryKey: ["pedido", pedidoId],
    queryFn: () => fetchPedido(pedidoId as number),
    enabled: pedidoId != null,
  });

  if (pedidoId == null) {
    return (
      <p style={{ fontSize: 12, color: colors.grayNeutral, margin: "6px 0 0" }}>
        Venta cargada directamente, sin detalle de productos.
      </p>
    );
  }

  if (isLoading) {
    return <p style={{ fontSize: 12, color: colors.grayNeutral, margin: "6px 0 0" }}>Cargando...</p>;
  }

  return (
    <ul style={{ margin: "6px 0 0", paddingLeft: 18, fontSize: 12 }}>
      {(pedido?.detalles ?? []).map((d) => (
        <li key={d.id}>
          {d.producto?.cod_producto} — {d.producto?.descripcion ?? ""} × {d.cantidad}
        </li>
      ))}
    </ul>
  );
}
