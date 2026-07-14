import { NavLink } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";
import { colors } from "../theme/colors";

interface NavItem {
  label: string;
  path: string;
  adminOnly?: boolean;
}

const NAV_ITEMS: NavItem[] = [
  { label: "Dashboard", path: "/dashboard" },
  { label: "Clientes", path: "/clientes" },
  { label: "Productos", path: "/productos" },
  { label: "Pedidos", path: "/pedidos" },
  { label: "Ventas", path: "/ventas" },
  { label: "Stock", path: "/stock" },
  { label: "Visitas y Agenda", path: "/visitas" },
  { label: "Importación Masiva", path: "/importacion" },
  { label: "Usuarios", path: "/usuarios", adminOnly: true },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

export function Sidebar({ open, onClose }: SidebarProps) {
  const { usuario } = useAuth();

  return (
    <aside
      className={`sidebar ${open ? "sidebar--open" : ""}`}
      style={{
        width: 240,
        background: colors.white,
        borderRadius: "0 24px 24px 0",
        boxShadow: "0 0 24px rgba(108,93,209,0.08)",
        padding: "24px 16px",
        display: "flex",
        flexDirection: "column",
        gap: 4,
      }}
    >
      <div style={{ padding: "0 12px 20px", fontWeight: 700, color: colors.purpleDark, fontSize: 18 }}>
        LUCMA
      </div>
      {NAV_ITEMS.filter((item) => !item.adminOnly || usuario?.rol === "Admin").map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          onClick={onClose}
          style={({ isActive }) => ({
            padding: "12px 16px",
            borderRadius: 14,
            textDecoration: "none",
            fontSize: 14,
            fontWeight: 600,
            color: isActive ? colors.white : "#4a4a5a",
            background: isActive ? colors.gradientBackground : "transparent",
          })}
        >
          {item.label}
        </NavLink>
      ))}
    </aside>
  );
}
