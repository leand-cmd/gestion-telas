import { Navigate, Route, Routes } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import { AdminRoute } from "./auth/AdminRoute";
import { AuthProvider } from "./auth/AuthContext";
import { LoginPage } from "./auth/LoginPage";
import { ProtectedRoute } from "./auth/ProtectedRoute";
import { Layout } from "./components/Layout";
import { DashboardPage } from "./features/dashboard/DashboardPage";
import { ClientesList } from "./features/clientes/ClientesList";
import { ImportacionPage } from "./features/importacion/ImportacionPage";
import { PedidosList } from "./features/pedidos/PedidosList";
import { ProductosList } from "./features/productos/ProductosList";
import { StockList } from "./features/stock/StockList";
import { UsuariosList } from "./features/usuarios/UsuariosList";
import { VentasList } from "./features/ventas/VentasList";
import { VisitasList } from "./features/visitas/VisitasList";
import { colors } from "./theme/colors";

export function App() {
  return (
    <AuthProvider>
      <Toaster
        position="top-right"
        toastOptions={{
          style: { borderRadius: 16 },
          success: { iconTheme: { primary: colors.purplePrimary, secondary: colors.white } },
        }}
      />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/clientes" element={<ClientesList />} />
            <Route path="/productos" element={<ProductosList />} />
            <Route path="/pedidos" element={<PedidosList />} />
            <Route path="/ventas" element={<VentasList />} />
            <Route path="/stock" element={<StockList />} />
            <Route path="/visitas" element={<VisitasList />} />
            <Route path="/importacion" element={<ImportacionPage />} />
            <Route element={<AdminRoute />}>
              <Route path="/usuarios" element={<UsuariosList />} />
            </Route>
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}
