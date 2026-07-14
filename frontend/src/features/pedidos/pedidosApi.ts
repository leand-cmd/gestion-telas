import { apiClient } from "../../api/client";
import type { Pedido, PedidoEstado, Venta, PaginatedResponse } from "../../api/types";

export interface PedidoFilters {
  estado?: string;
  cliente_id?: number;
  page?: number;
  per_page?: number;
}

export async function fetchPedidos(filters: PedidoFilters) {
  const { data } = await apiClient.get<PaginatedResponse<Pedido>>("/pedidos", { params: filters });
  return data;
}

export async function fetchPedido(id: number) {
  const { data } = await apiClient.get<Pedido>(`/pedidos/${id}`);
  return data;
}

export interface PedidoDetalleInput {
  producto_id: number;
  cantidad: number;
  valor_unitario?: number | null;
}

export interface PedidoInput {
  cliente_id: number;
  tipo_compra?: string | null;
  fecha_pedido?: string | null;
  fecha_entrega_estimada?: string | null;
  observaciones?: string | null;
  detalles: PedidoDetalleInput[];
}

export async function createPedido(input: PedidoInput) {
  const { data } = await apiClient.post<Pedido>("/pedidos", input);
  return data;
}

export async function updatePedido(id: number, input: Partial<PedidoInput>) {
  const { data } = await apiClient.put<Pedido>(`/pedidos/${id}`, input);
  return data;
}

export async function deletePedido(id: number) {
  await apiClient.delete(`/pedidos/${id}`);
}

export async function cambiarEstadoPedido(id: number, estado: PedidoEstado) {
  const { data } = await apiClient.patch<Pedido>(`/pedidos/${id}/estado`, { estado });
  return data;
}

export async function convertirPedidoAVenta(id: number) {
  const { data } = await apiClient.post<Venta>(`/pedidos/${id}/convertir-a-venta`);
  return data;
}

export async function enviarEmailPedido(id: number) {
  const { data } = await apiClient.post<{ status: string }>(`/pedidos/${id}/email`);
  return data;
}

export async function descargarPdfPedido(id: number, nroPedido: string) {
  const { data } = await apiClient.get(`/pedidos/${id}/pdf`, { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  link.href = url;
  link.download = `${nroPedido}.pdf`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

export async function exportPedidos() {
  const { data } = await apiClient.get("/pedidos/export", { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  link.href = url;
  link.download = "pedidos.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}
