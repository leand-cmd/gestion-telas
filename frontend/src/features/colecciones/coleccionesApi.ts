import { apiClient } from "../../api/client";
import type { Coleccion, PaginatedResponse } from "../../api/types";

export async function fetchColecciones() {
  const { data } = await apiClient.get<PaginatedResponse<Coleccion>>("/colecciones", {
    params: { per_page: 100 },
  });
  return data;
}

export type ColeccionInput = Omit<Coleccion, "id" | "created_at" | "updated_at">;

export async function createColeccion(input: ColeccionInput) {
  const { data } = await apiClient.post<Coleccion>("/colecciones", input);
  return data;
}

export async function updateColeccion(id: number, input: Partial<ColeccionInput>) {
  const { data } = await apiClient.put<Coleccion>(`/colecciones/${id}`, input);
  return data;
}

export async function deleteColeccion(id: number) {
  await apiClient.delete(`/colecciones/${id}`);
}

export async function uploadImagenColeccion(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await apiClient.post<{ url: string }>("/colecciones/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data.url;
}
