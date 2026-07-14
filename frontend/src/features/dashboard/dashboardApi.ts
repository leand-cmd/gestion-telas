import { apiClient } from "../../api/client";
import type { DashboardResumen } from "../../api/types";

export async function fetchResumen() {
  const { data } = await apiClient.get<DashboardResumen>("/dashboard/resumen");
  return data;
}
