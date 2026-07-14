import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import { colors } from "../theme/colors";
import { useAuth } from "./AuthContext";

export function LoginPage() {
  const { login, register } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [nombre, setNombre] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register(email, password, nombre);
      }
      navigate("/");
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo completar la operacion");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: colors.gradientBackground,
        padding: 24,
      }}
    >
      <form
        onSubmit={handleSubmit}
        className="card"
        style={{ width: "100%", maxWidth: 400, display: "flex", flexDirection: "column", gap: 16 }}
      >
        <div style={{ textAlign: "center", marginBottom: 8 }}>
          <h1 style={{ margin: 0, color: colors.purpleDark, fontSize: 24 }}>LUCMA</h1>
          <p style={{ margin: "4px 0 0", color: colors.grayNeutral, fontSize: 13 }}>
            Gestión de Ventas — Telas
          </p>
        </div>

        {mode === "register" && (
          <div>
            <label htmlFor="nombre">Nombre</label>
            <input
              id="nombre"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
          </div>
        )}

        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? "Procesando..." : mode === "login" ? "Ingresar" : "Crear cuenta"}
        </button>

        <button
          type="button"
          className="btn btn-secondary"
          onClick={() => setMode(mode === "login" ? "register" : "login")}
        >
          {mode === "login" ? "Crear una cuenta nueva" : "Ya tengo una cuenta"}
        </button>
      </form>
    </div>
  );
}
