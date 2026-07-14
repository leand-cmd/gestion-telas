import { apiClient } from "../../api/client";
import type { ImportReport, PaginatedResponse, Producto } from "../../api/types";

export interface ProductoFilters {
  q?: string;
  categoria?: string;
  estado?: string;
  page?: number;
  per_page?: number;
}

export async function fetchProductos(filters: ProductoFilters) {
  const { data } = await apiClient.get<PaginatedResponse<Producto>>("/productos", {
    params: filters,
  });
  return data;
}

export type ProductoInput = Omit<
  Producto,
  "id" | "created_at" | "updated_at" | "imagen_url"
>;

export async function createProducto(input: ProductoInput) {
  const { data } = await apiClient.post<Producto>("/productos", input);
  return data;
}

export async function updateProducto(id: number, input: Partial<ProductoInput>) {
  const { data } = await apiClient.put<Producto>(`/productos/${id}`, input);
  return data;
}

export async function deleteProducto(id: number) {
  await apiClient.delete(`/productos/${id}`);
}

export async function uploadProductoImagen(id: number, file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await apiClient.post<Producto>(`/productos/${id}/imagen`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function importProductos(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await apiClient.post<ImportReport>("/productos/import", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function exportProductos() {
  const { data } = await apiClient.get("/productos/export", { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  link.href = url;
  link.download = "productos.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}
