import type { VisitaEstado } from "../../api/types";

const ESTADO_COLORS_MAP: Record<VisitaEstado, { bg: string; text: string; dot: string }> = {
  programada: { bg: "#E7F0FE", text: "#1D4ED8", dot: "#3B82F6" },
  realizada: { bg: "#E6F7EC", text: "#15803D", dot: "#22C55E" },
  cancelada: { bg: "#FDECEC", text: "#B91C1C", dot: "#EF4444" },
};

const ESTADO_COLOR_DESCONOCIDO = { bg: "#F5F5F7", text: "#4a4a5a", dot: "#999999" };

const ESTADO_LABELS_MAP: Record<VisitaEstado, string> = {
  programada: "Programada",
  realizada: "Realizada",
  cancelada: "Cancelada",
};

// Acceso seguro: si estado no matchea ninguna clave conocida (dato viejo o
// inesperado), devuelve un color/label neutro en vez de romper el render.
export function colorParaEstadoVisita(estado: VisitaEstado | string) {
  return ESTADO_COLORS_MAP[estado as VisitaEstado] ?? ESTADO_COLOR_DESCONOCIDO;
}

export function labelParaEstadoVisita(estado: VisitaEstado | string) {
  return ESTADO_LABELS_MAP[estado as VisitaEstado] ?? estado;
}
