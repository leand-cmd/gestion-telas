import { useState } from "react";
import toast from "react-hot-toast";

import type { ImportReport } from "../api/types";
import { colors } from "../theme/colors";

interface ImportModalProps {
  title: string;
  onImport: (file: File) => Promise<ImportReport>;
  onClose: () => void;
  onImported: () => void;
}

export function ImportModal({ title, onImport, onClose, onImported }: ImportModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [report, setReport] = useState<ImportReport | null>(null);
  const [loading, setLoading] = useState(false);

  const handleImport = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const result = await onImport(file);
      setReport(result);
      toast.success(`${result.insertados} registros importados`);
      onImported();
    } catch (err: any) {
      toast.error(err?.response?.data?.error || "Error al importar el archivo");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="card modal-card" style={{ maxWidth: 460 }}>
        <h3 style={{ marginTop: 0, color: colors.purpleDark }}>{title}</h3>
        <p style={{ fontSize: 13, color: colors.grayNeutral }}>
          Archivos soportados: .csv, .xlsx, .xls
        </p>

        <input
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />

        {report && (
          <div
            style={{
              marginTop: 16,
              padding: 12,
              borderRadius: 12,
              background: colors.grayLight,
              fontSize: 13,
              maxHeight: 200,
              overflowY: "auto",
            }}
          >
            <p style={{ margin: 0 }}>
              Filas procesadas: {report.total_filas} · Insertados: {report.insertados} ·
              Errores: {report.cantidad_errores}
            </p>
            {report.errores.length > 0 && (
              <ul style={{ margin: "8px 0 0", paddingLeft: 18 }}>
                {report.errores.map((e, idx) => (
                  <li key={idx}>
                    Fila {e.fila}: {JSON.stringify(e.error)}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 20 }}>
          <button className="btn btn-secondary" onClick={onClose}>
            Cerrar
          </button>
          <button
            className="btn btn-primary"
            onClick={handleImport}
            disabled={!file || loading}
          >
            {loading ? "Importando..." : "Importar"}
          </button>
        </div>
      </div>
    </div>
  );
}
