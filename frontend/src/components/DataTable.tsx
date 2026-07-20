import { ReactNode } from "react";

import { colors } from "../theme/colors";

export interface Column<T> {
  header: string;
  render: (row: T) => ReactNode;
  truncate?: boolean;
  minWidth?: number;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  rows: T[];
  rowKey: (row: T) => string | number;
  loading?: boolean;
  emptyMessage?: string;
}

export function DataTable<T>({
  columns,
  rows,
  rowKey,
  loading,
  emptyMessage = "Sin resultados",
}: DataTableProps<T>) {
  if (loading) {
    return (
      <div style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>
        Cargando...
      </div>
    );
  }

  if (rows.length === 0) {
    return (
      <div style={{ padding: 40, textAlign: "center", color: colors.grayNeutral }}>
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.header} style={col.minWidth ? { minWidth: col.minWidth } : undefined}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={rowKey(row)}>
              {columns.map((col) => (
                <td key={col.header} className={col.truncate ? "td-truncate" : undefined}>
                  {col.render(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
