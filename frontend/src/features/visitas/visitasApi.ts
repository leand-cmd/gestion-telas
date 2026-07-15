import { apiClient } from "../../api/client";
import type { PaginatedResponse, Visita } from "../../api/types";

export interface VisitaFilters {
  desde?: string;
  hasta?: string;
  asesor_id?: number;
  cliente_id?: number;
  estado?: string;
  page?: number;
  per_page?: number;
}

export async function fetchVisitas(filters: VisitaFilters) {
  const { data } = await apiClient.get<PaginatedResponse<Visita>>("/visitas", { params: filters });
  return data;
}

export interface VisitaInput {
  cliente_id: number;
  asesor_id: number;
  fecha: string;
  hora: string;
  proposito?: string | null;
  direccion?: string | null;
  notas_previas?: string | null;
}

export async function createVisita(input: VisitaInput) {
  const { data } = await apiClient.post<Visita>("/visitas", input);
  return data;
}

export async function updateVisita(id: number, input: Partial<VisitaInput>) {
  const { data } = await apiClient.put<Visita>(`/visitas/${id}`, input);
  return data;
}

export interface VisitaResultadoInput {
  resultado: string;
  tipo_gestion?: string | null;
  duracion_actual?: number | null;
  presente_cliente?: boolean | null;
  productos_presentados?: string | null;
  notas_visita?: string | null;
  proxima_accion?: string | null;
}

export async function registrarResultado(id: number, input: VisitaResultadoInput) {
  const { data } = await apiClient.patch<Visita>(`/visitas/${id}/resultado`, input);
  return data;
}

export async function deleteVisita(id: number) {
  await apiClient.delete(`/visitas/${id}`);
}

export async function cancelarVisita(id: number) {
  const { data } = await apiClient.patch<Visita>(`/visitas/${id}/cancelar`);
  return data;
}
