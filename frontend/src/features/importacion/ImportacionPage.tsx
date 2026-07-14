import { useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { ImportModal } from "../../components/ImportModal";
import { colors } from "../../theme/colors";
import { exportClientes, importClientes } from "../clientes/clientesApi";
import { exportProductos, importProductos } from "../productos/productosApi";

type Entidad = "clientes" | "productos";

const ENTIDADES: { value: Entidad; label: string }[] = [
  { value: "clientes", label: "Clientes" },
  { value: "productos", label: "Productos" },
];

export function ImportacionPage() {
  const [entidad, setEntidad] = useState<Entidad>("clientes");
  const [importOpen, setImportOpen] = useState(false);
  const queryClient = useQueryClient();

  const config =
    entidad === "clientes"
      ? { onImport: importClientes, onExport: exportClientes, queryKey: "clientes" }
      : { onImport: importProductos, onExport: exportProductos, queryKey: "productos" };

  return (
    <div>
      <h2 style={{ margin: "0 0 16px", color: colors.purpleDark }}>Importación Masiva</h2>

      <div className="card" style={{ display: "flex", flexDirection: "column", gap: 16, maxWidth: 480 }}>
        <div>
          <label htmlFor="entidad">Entidad a importar/exportar</label>
          <select id="entidad" value={entidad} onChange={(e) => setEntidad(e.target.value as Entidad)}>
            {ENTIDADES.map((e) => (
              <option key={e.value} value={e.value}>
                {e.label}
              </option>
            ))}
          </select>
        </div>

        <p style={{ fontSize: 13, color: colors.grayNeutral, margin: 0 }}>
          Formatos soportados: .csv, .xlsx, .xls. Exportá primero para usar el archivo como
          plantilla de referencia.
        </p>

        <div style={{ display: "flex", gap: 8 }}>
          <button
            className="btn btn-secondary"
            onClick={() => config.onExport().catch(() => toast.error("Error al exportar"))}
          >
            Exportar {entidad}
          </button>
          <button className="btn btn-primary" onClick={() => setImportOpen(true)}>
            Importar {entidad}
          </button>
        </div>
      </div>

      {importOpen && (
        <ImportModal
          title={`Importar ${entidad}`}
          onImport={config.onImport}
          onClose={() => setImportOpen(false)}
          onImported={() => queryClient.invalidateQueries({ queryKey: [config.queryKey] })}
        />
      )}
    </div>
  );
}
