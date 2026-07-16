import { colors } from "../../theme/colors";

// Orden fijo por tipo de gestion (no ciclado), para que cada categoria
// mantenga siempre el mismo color sin importar el orden de los datos.
export const GESTION_COLORS: Record<string, string> = {
  "Solicita Muestras": "#9B8FE0",
  "Entrega de Muestras": colors.purpleIcons,
  "Venta Exitosa": colors.purplePrimary,
  "Sin Contacto": colors.grayNeutral,
  "Visita Cancelada": colors.pinkNeon,
  "Visita Reprogramada": colors.pinkLight,
  "Visita de Seguimiento": colors.purpleDark,
  "Visita sin éxito": "#C2185B",
};

export function colorForTipoGestion(tipo: string): string {
  return GESTION_COLORS[tipo] ?? colors.grayNeutral;
}
