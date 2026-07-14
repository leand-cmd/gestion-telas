import { useAuth } from "../auth/AuthContext";
import { colors } from "../theme/colors";

interface HeaderProps {
  onMenuClick: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  const { usuario, logout } = useAuth();

  return (
    <header
      className="header-bar"
      style={{
        background: colors.gradientBackground,
        borderRadius: 24,
        padding: "16px 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        color: colors.white,
        marginBottom: 24,
        gap: 12,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 14, minWidth: 0 }}>
        <button className="hamburger-btn" onClick={onMenuClick} aria-label="Abrir menú">
          ☰
        </button>
        <img
          src="/img/asesora.jpg"
          alt=""
          style={{
            width: 64,
            height: 64,
            borderRadius: "50%",
            objectFit: "cover",
            objectPosition: "center",
            border: "2px solid rgba(255,255,255,0.6)",
            flexShrink: 0,
          }}
        />
        <div style={{ minWidth: 0 }}>
          <div className="header-name" style={{ fontWeight: 700, fontSize: 15, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
            {usuario?.nombre}
          </div>
          <div style={{ fontSize: 12, opacity: 0.85 }}>{usuario?.rol}</div>
        </div>
      </div>

      <button
        onClick={logout}
        className="btn"
        style={{ background: "rgba(255,255,255,0.2)", color: colors.white, flexShrink: 0 }}
      >
        Salir
      </button>
    </header>
  );
}
