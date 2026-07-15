import { colors } from "../../theme/colors";

// Orden fijo por tipo de gestion (no ciclado), para que cada categoria
// mantenga siempre el mismo color sin importar el orden de los datos.
export const GESTION_COLORS: Record<string, string> = {
  "Visita Exitosa - Carga de pedido": colors.purplePrimary,
  "Cliente sobrestockeado": colors.purpleIcons,
  "Requiere seguimiento": colors.pinkLight,
  "No fue posible contactar": colors.grayNeutral,
  "Cliente cambió proveedor": colors.pinkNeon,
  Otro: colors.purpleDark,
};

export function colorForTipoGestion(tipo: string): string {
  return GESTION_COLORS[tipo] ?? colors.grayNeutral;
}
