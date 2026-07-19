import { apiClient } from "../../api/client";
import type { PaginatedResponse, StockItem, StockMovimiento, StockMovimientoTipo } from "../../api/types";

export interface StockFilters {
  q?: string;
  page?: number;
  per_page?: number;
}

export async function fetchStock(filters: StockFilters) {
  const { data } = await apiClient.get<PaginatedResponse<StockItem>>("/stock", { params: filters });
  return data;
}

export async function fetchMovimientos(producto_id: number, page = 1) {
  const { data } = await apiClient.get<PaginatedResponse<StockMovimiento>>("/stock/movimientos", {
    params: { producto_id, page, per_page: 20 },
  });
  return data;
}

export interface MovimientoInput {
  producto_id: number;
  tipo: StockMovimientoTipo;
  cantidad: number;
  motivo?: string | null;
}

export async function crearMovimiento(input: MovimientoInput) {
  const { data } = await apiClient.post<StockMovimiento>("/stock/movimientos", input);
  return data;
}
