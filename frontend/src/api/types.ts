export interface Usuario {
  id: number;
  email: string;
  nombre: string;
  rol: "Admin" | "Asesor Comercial" | "Gerente" | "Vendedor";
  foto_url: string | null;
  activo: boolean;
  created_at: string;
}

export interface Cliente {
  id: number;
  codigo_cliente: string | null;
  ruc: string | null;
  razon_social: string;
  localidad: string | null;
  barrio: string | null;
  direccion: string | null;
  telefono: string | null;
  email: string | null;
  canal: string | null;
  sub_canal: string | null;
  tipo_compra: string | null;
  latitude: number | null;
  longitude: number | null;
  lista_precios_id: number | null;
  estado: boolean;
  created_at: string;
  updated_at: string;
}

export interface Producto {
  id: number;
  cod_producto: string;
  marca: string | null;
  linea: string | null;
  categoria: string | null;
  subcategoria: string | null;
  cod_color: string | null;
  color: string | null;
  color_categoria: string | null;
  codigo_base: string | null;
  descripcion_completa: string | null;
  diseno: string | null;
  medida: string | null;
  piezas: number | null;
  precio: number | null;
  stock_actual: number;
  stock_minimo: number | null;
  estado: boolean;
  imagen_url: string | null;
  origen: string | null;
  created_at: string;
  updated_at: string;
}

export interface PedidoDetalle {
  id: number;
  pedido_id: number;
  producto_id: number;
  producto: Producto | null;
  cantidad: number;
  metros: number | null;
  kilogramos: number | null;
  valor_unitario: number | null;
  subtotal: number | null;
}

export type PedidoEstado = "Pendiente" | "Confirmado" | "Entregado" | "Facturado" | "Cancelado";

export interface Pedido {
  id: number;
  nro_pedido: string;
  cliente_id: number;
  cliente: Cliente | null;
  tipo_compra: string | null;
  fecha_pedido: string | null;
  fecha_entrega_estimada: string | null;
  total: number;
  observaciones: string | null;
  estado: PedidoEstado;
  detalles?: PedidoDetalle[];
  created_at: string;
  updated_at: string;
}

export type VentaEstadoPago = "pendiente" | "pagado" | "vencido";

export interface Venta {
  id: number;
  nro_factura: string;
  pedido_id: number | null;
  cliente_id: number;
  cliente: Cliente | null;
  fecha_factura: string | null;
  fecha_entrega: string | null;
  total: number;
  tipo_compra: string | null;
  estado_pago: VentaEstadoPago;
  observaciones: string | null;
  created_at: string;
  updated_at: string;
}

export interface StockItem extends Producto {
  bajo_minimo: boolean;
}

export type StockMovimientoTipo = "entrada" | "salida" | "ajuste";

export interface StockMovimiento {
  id: number;
  producto_id: number;
  producto: Producto | null;
  tipo: StockMovimientoTipo;
  cantidad: number;
  motivo: string | null;
  venta_id: number | null;
  created_at: string;
}

export type VisitaEstado = "programada" | "realizada" | "cancelada";

export interface Visita {
  id: number;
  cliente_id: number;
  cliente: Cliente | null;
  asesor_id: number;
  asesor: Usuario | null;
  fecha: string;
  hora: string | null;
  proposito: string | null;
  direccion: string | null;
  notas_previas: string | null;
  estado: VisitaEstado;
  duracion_actual: number | null;
  presente_cliente: boolean | null;
  productos_presentados: string | null;
  resultado: string | null;
  tipo_gestion: string | null;
  notas_visita: string | null;
  proxima_accion: string | null;
  created_at: string;
  updated_at: string;
}

export interface DashboardResumen {
  ventas_mes_actual: number;
  ventas_por_mes: { mes: string; total: number }[];
  pedidos_pendientes: number;
  stock_bajo: Producto[];
  proximas_visitas: Visita[];
  top_clientes: { cliente: Cliente; total_ventas: number }[];
  top_productos: { producto: Producto; cantidad_total: number }[];
  total_clientes_cartera: number;
  clientes_visitados_mes: number;
  cobertura_porcentaje: number;
  gestiones_por_tipo: { tipo: string; cantidad: number }[];
  efectividad_gestiones_porcentaje: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  per_page: number;
  total: number;
  pages: number;
}

export interface ImportReport {
  total_filas: number;
  insertados: number;
  errores: { fila: number; error: unknown }[];
  cantidad_errores: number;
}
