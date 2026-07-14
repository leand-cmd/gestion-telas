import { colors } from "../theme/colors";

interface PaginationProps {
  page: number;
  pages: number;
  total: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ page, pages, total, onPageChange }: PaginationProps) {
  if (pages <= 1) return null;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        marginTop: 16,
        fontSize: 13,
        color: colors.grayNeutral,
      }}
    >
      <span>
        Página {page} de {pages} · {total} registros
      </span>
      <div style={{ display: "flex", gap: 8 }}>
        <button
          className="btn btn-secondary"
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
        >
          Anterior
        </button>
        <button
          className="btn btn-secondary"
          disabled={page >= pages}
          onClick={() => onPageChange(page + 1)}
        >
          Siguiente
        </button>
      </div>
    </div>
  );
}
