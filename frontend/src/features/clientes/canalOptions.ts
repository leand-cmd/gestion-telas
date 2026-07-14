export const CANALES = ["Mayorista", "Minorista", "Distribuidora", "Fabricante"] as const;
export const TIPOS_COMPRA = ["Contado", "Credito", "Cheque"] as const;

export const SUB_CANALES_POR_CANAL: Record<string, string[]> = {
  Mayorista: ["Grandes cuentas", "Cadenas", "Cooperativas"],
  Minorista: ["Comercio de barrio", "Boutique", "Feria"],
  Distribuidora: ["Regional", "Nacional"],
  Fabricante: ["Confeccionista", "Industrial"],
};
