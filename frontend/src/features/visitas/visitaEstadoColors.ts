import type { VisitaEstado } from "../../api/types";

export const ESTADO_COLORS: Record<VisitaEstado, { bg: string; text: string; dot: string }> = {
  programada: { bg: "#E7F0FE", text: "#1D4ED8", dot: "#3B82F6" },
  realizada: { bg: "#E6F7EC", text: "#15803D", dot: "#22C55E" },
  cancelada: { bg: "#FDECEC", text: "#B91C1C", dot: "#EF4444" },
};

export const ESTADO_LABELS: Record<VisitaEstado, string> = {
  programada: "Programada",
  realizada: "Realizada",
  cancelada: "Cancelada",
};
