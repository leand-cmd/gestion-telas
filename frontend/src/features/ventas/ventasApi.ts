import { apiClient } from "../../api/client";
import type { PaginatedResponse, Venta, VentaEstadoPago } from "../../api/types";

export interface VentaFilters {
  estado_pago?: string;
  cliente_id?: number;
  desde?: string;
  hasta?: string;
  page?: number;
  per_page?: number;
}

export async function fetchVentas(filters: VentaFilters) {
  const { data } = await apiClient.get<PaginatedResponse<Venta>>("/ventas", { params: filters });
  return data;
}

export interface VentaInput {
  cliente_id: number;
  total: number;
  fecha_factura?: string | null;
  fecha_entrega?: string | null;
  tipo_compra?: string | null;
  observaciones?: string | null;
}

export async function createVenta(input: VentaInput) {
  const { data } = await apiClient.post<Venta>("/ventas", input);
  return data;
}

export async function updateVenta(id: number, input: Partial<VentaInput>) {
  const { data } = await apiClient.put<Venta>(`/ventas/${id}`, input);
  return data;
}

export async function cambiarEstadoPago(id: number, estado_pago: VentaEstadoPago) {
  const { data } = await apiClient.patch<Venta>(`/ventas/${id}/estado-pago`, { estado_pago });
  return data;
}

export async function deleteVenta(id: number) {
  await apiClient.delete(`/ventas/${id}`);
}

export async function descargarPdfVenta(id: number, nroFactura: string) {
  const { data } = await apiClient.get(`/ventas/${id}/pdf`, { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  link.href = url;
  link.download = `${nroFactura}.pdf`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

export async function exportVentas() {
  const { data } = await apiClient.get("/ventas/export", { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  link.href = url;
  link.download = "ventas.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}
