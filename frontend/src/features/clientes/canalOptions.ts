export const CANALES = [
  "Mayorista",
  "Minorista",
  "Alta Costura",
  "Deportivo",
  "Uniformes",
] as const;

export const SUBCANALES_POR_CANAL: Record<(typeof CANALES)[number], readonly string[]> = {
  Mayorista: ["Distribuidor nacional", "Distribuidor internacional", "Importador"],
  Minorista: ["Tienda física", "Tienda online", "Showroom"],
  "Alta Costura": ["Diseñador independiente", "Atelier", "Boutique exclusiva"],
  Deportivo: ["Marca deportiva", "Fabricante ropa deportiva", "Distribuidor deportivo"],
  Uniformes: [
    "Uniformes médicos",
    "Uniformes oficina",
    "Uniformes industriales",
    "Uniformes escolares",
  ],
};

export const TIPOS_COMPRA = ["Contado", "Credito", "Cheque"] as const;
