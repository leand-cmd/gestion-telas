import { useAuth } from "../auth/AuthContext";
import { colors } from "../theme/colors";

export function Header() {
  const { usuario, logout } = useAuth();

  return (
    <header
      style={{
        background: colors.gradientBackground,
        borderRadius: 24,
        padding: "16px 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        color: colors.white,
        marginBottom: 24,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <img
          src="/assets/asesora-placeholder.svg"
          alt="Asesora Comercial"
          style={{ width: 48, height: 48, borderRadius: "50%", border: "2px solid rgba(255,255,255,0.6)" }}
        />
        <div>
          <div style={{ fontWeight: 700, fontSize: 15 }}>Nombre Asesora</div>
          <div style={{ fontSize: 12, opacity: 0.85 }}>Asesora Comercial</div>
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontWeight: 600, fontSize: 13 }}>{usuario?.nombre}</div>
          <div style={{ fontSize: 11, opacity: 0.8 }}>{usuario?.rol}</div>
        </div>
        <button
          onClick={logout}
          className="btn"
          style={{ background: "rgba(255,255,255,0.2)", color: colors.white }}
        >
          Salir
        </button>
      </div>
    </header>
  );
}
