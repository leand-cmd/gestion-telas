import { FormEvent, useState } from "react";
import toast from "react-hot-toast";

import type { Usuario } from "../../api/types";
import { colors } from "../../theme/colors";
import { ROLES } from "./usuarioOptions";
import { createUsuario, updateUsuario, type UsuarioInput } from "./usuariosApi";

interface UsuarioFormProps {
  usuario: Usuario | null;
  onClose: () => void;
  onSaved: () => void;
}

export function UsuarioForm({ usuario, onClose, onSaved }: UsuarioFormProps) {
  const [form, setForm] = useState<UsuarioInput>({
    email: usuario?.email ?? "",
    password: "",
    nombre: usuario?.nombre ?? "",
    rol: usuario?.rol ?? "Vendedor",
  });
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (usuario) {
        const { password, ...rest } = form;
        await updateUsuario(usuario.id, password ? form : rest);
        toast.success("Usuario actualizado");
      } else {
        await createUsuario(form);
        toast.success("Usuario creado");
      }
      onSaved();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "No se pudo guardar el usuario");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(43,43,56,0.4)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        padding: 24,
      }}
    >
      <form
        onSubmit={handleSubmit}
        className="card"
        style={{ width: "100%", maxWidth: 420, display: "flex", flexDirection: "column", gap: 14 }}
      >
        <h3 style={{ margin: 0, color: colors.purpleDark }}>
          {usuario ? "Editar usuario" : "Nuevo usuario"}
        </h3>

        <div>
          <label htmlFor="nombre">Nombre</label>
          <input
            id="nombre"
            value={form.nombre}
            onChange={(e) => setForm({ ...form, nombre: e.target.value })}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            required
          />
        </div>
        <div>
          <label htmlFor="password">
            Contraseña {usuario ? "(dejar vacío para no cambiar)" : ""}
          </label>
          <input
            id="password"
            type="password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required={!usuario}
            minLength={6}
          />
        </div>
        <div>
          <label htmlFor="rol">Rol</label>
          <select
            id="rol"
            value={form.rol}
            onChange={(e) => setForm({ ...form, rol: e.target.value as Usuario["rol"] })}
          >
            {ROLES.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 8 }}>
          <button type="button" className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? "Guardando..." : "Guardar"}
          </button>
        </div>
      </form>
    </div>
  );
}
