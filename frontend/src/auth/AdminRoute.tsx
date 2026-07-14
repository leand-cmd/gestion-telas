import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "./AuthContext";

export function AdminRoute() {
  const { usuario } = useAuth();
  if (usuario?.rol !== "Admin") {
    return <Navigate to="/dashboard" replace />;
  }
  return <Outlet />;
}
