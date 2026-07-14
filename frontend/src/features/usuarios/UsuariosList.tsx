import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { Column, DataTable } from "../../components/DataTable";
import { Pagination } from "../../components/Pagination";
import type { Usuario } from "../../api/types";
import { colors } from "../../theme/colors";
import { UsuarioForm } from "./UsuarioForm";
import { cambiarEstadoUsuario, fetchUsuarios } from "./usuariosApi";

export function UsuariosList() {
  const [page, setPage] = useState(1);
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Usuario | null>(null);

  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["usuarios", { page }],
    queryFn: () => fetchUsuarios({ page, per_page: 10 }),
  });

  const refetch = () => queryClient.invalidateQueries({ queryKey: ["usuarios"] });

  const toggleEstado = async (u: Usuario) => {
    try {
      await cambiarEstadoUsuario(u.id, !u.activo);
      toast.success(u.activo ? "Usuario desactivado" : "Usuario activado");
      refetch();
    } catch {
      toast.error("No se pudo cambiar el estado");
    }
  };

  const columns: Column<Usuario>[] = [
    { header: "Nombre", render: (u) => u.nombre, truncate: true },
    { header: "Email", render: (u) => u.email, truncate: true },
    { header: "Rol", render: (u) => u.rol },
    {
      header: "Estado",
      render: (u) => (
        <span className={`badge ${u.activo ? "badge-active" : "badge-inactive"}`}>
          {u.activo ? "Activo" : "Inactivo"}
        </span>
      ),
    },
    {
      header: "Acciones",
      render: (u) => (
        <div style={{ display: "flex", gap: 8 }}>
          <button
            className="btn btn-secondary"
            onClick={() => {
              setEditing(u);
              setFormOpen(true);
            }}
          >
            Editar
          </button>
          <button
            className={`btn ${u.activo ? "btn-danger" : "btn-secondary"}`}
            onClick={() => toggleEstado(u)}
          >
            {u.activo ? "Desactivar" : "Activar"}
          </button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 16,
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <h2 style={{ margin: 0, color: colors.purpleDark }}>Usuarios</h2>
        <button
          className="btn btn-primary"
          onClick={() => {
            setEditing(null);
            setFormOpen(true);
          }}
        >
          + Nuevo Usuario
        </button>
      </div>

      <div className="card">
        <DataTable
          columns={columns}
          rows={data?.items ?? []}
          rowKey={(u) => u.id}
          loading={isLoading}
          emptyMessage="No se encontraron usuarios"
        />
        {data && (
          <Pagination page={data.page} pages={data.pages} total={data.total} onPageChange={setPage} />
        )}
      </div>

      {formOpen && (
        <UsuarioForm
          usuario={editing}
          onClose={() => setFormOpen(false)}
          onSaved={() => {
            setFormOpen(false);
            refetch();
          }}
        />
      )}
    </div>
  );
}
