import { createContext, ReactNode, useContext, useState } from "react";

import { apiClient } from "../api/client";
import type { Usuario } from "../api/types";

interface AuthContextValue {
  usuario: Usuario | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, nombre: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

function loadStoredUsuario(): Usuario | null {
  const raw = localStorage.getItem("usuario");
  if (!raw) return null;
  try {
    return JSON.parse(raw) as Usuario;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(loadStoredUsuario);

  const persistSession = (token: string, user: Usuario) => {
    localStorage.setItem("token", token);
    localStorage.setItem("usuario", JSON.stringify(user));
    setUsuario(user);
  };

  const login = async (email: string, password: string) => {
    const { data } = await apiClient.post("/auth/login", { email, password });
    persistSession(data.token, data.usuario);
  };

  const register = async (email: string, password: string, nombre: string) => {
    const { data } = await apiClient.post("/auth/register", { email, password, nombre });
    persistSession(data.token, data.usuario);
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    setUsuario(null);
  };

  return (
    <AuthContext.Provider
      value={{ usuario, isAuthenticated: !!usuario, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return ctx;
}
