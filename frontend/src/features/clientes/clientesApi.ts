import { apiClient } from "../../api/client";
import type { Cliente, ImportReport, PaginatedResponse } from "../../api/types";

export interface ClienteFilters {
  q?: string;
  canal?: string;
  estado?: string;
  page?: number;
  per_page?: number;
}

export async function fetchClientes(filters: ClienteFilters) {
  const { data } = await apiClient.get<PaginatedResponse<Cliente>>("/clientes", {
    params: filters,
  });
  return data;
}

export type ClienteInput = Omit<Cliente, "id" | "created_at" | "updated_at">;

export async function createCliente(input: ClienteInput) {
  const { data } = await apiClient.post<Cliente>("/clientes", input);
  return data;
}

export async function updateCliente(id: number, input: Partial<ClienteInput>) {
  const { data } = await apiClient.put<Cliente>(`/clientes/${id}`, input);
  return data;
}

export async function deleteCliente(id: number) {
  await apiClient.delete(`/clientes/${id}`);
}

export async function fetchNextClienteId() {
  const { data } = await apiClient.get<{ next_id: string }>("/clientes/next-id");
  return data.next_id;
}

export async function importClientes(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await apiClient.post<ImportReport>("/clientes/import", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function exportClientes() {
  const { data } = await apiClient.get("/clientes/export", { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  link.href = url;
  link.download = "clientes.csv";
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}
