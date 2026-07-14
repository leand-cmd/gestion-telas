import { apiClient } from "../../api/client";
import type { PaginatedResponse, Usuario } from "../../api/types";

export interface UsuarioInput {
  email: string;
  password?: string;
  nombre: string;
  rol: Usuario["rol"];
}

export async function fetchUsuarios(params: { page?: number; per_page?: number }) {
  const { data } = await apiClient.get<PaginatedResponse<Usuario>>("/usuarios", { params });
  return data;
}

export async function fetchAsesores() {
  const { data } = await apiClient.get<Usuario[]>("/usuarios/asesores");
  return data;
}

export async function createUsuario(input: UsuarioInput) {
  const { data } = await apiClient.post<Usuario>("/usuarios", input);
  return data;
}

export async function updateUsuario(id: number, input: Partial<UsuarioInput>) {
  const { data } = await apiClient.put<Usuario>(`/usuarios/${id}`, input);
  return data;
}

export async function cambiarEstadoUsuario(id: number, activo: boolean) {
  const { data } = await apiClient.patch<Usuario>(`/usuarios/${id}/estado`, { activo });
  return data;
}
