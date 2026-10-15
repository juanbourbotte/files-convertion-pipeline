from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


class DataValidator:
    """Diagnostica errores de tipeo o formato en columnas numéricas de datasets tabulares."""

    @staticmethod
    def inspect_numeric_columns(file_path: Path) -> Dict[str, Any]:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"El archivo no existe: {file_path}")

        # Cargar datos según extensión
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path, sep=None, engine="python")

        df.columns = df.columns.str.strip()

        # Identificar columnas potencialmente numéricas
        potential_numeric = []
        for col in df.columns:
            try:
                pd.to_numeric(df[col], errors="raise")
                potential_numeric.append(col)
            except Exception:
                if col.lower() in [
                    "td",
                    "speed",
                    "t.duration",
                    "tdt",
                    "cr",
                    "trackmate",
                ]:
                    potential_numeric.append(col)

        problems = []
        for col in potential_numeric:
            bad_mask = pd.to_numeric(df[col], errors="coerce").isna() & df[col].notna()
            bad_entries = df.loc[bad_mask, col]

            for idx, val in bad_entries.items():
                problems.append({
                    "column": col,
                    "row": idx + 2,  # Ajuste para coincidir con la fila del archivo (1-indexed + header)
                    "value": str(val)
                })

        return {
            "file": str(file_path),
            "columns_checked": potential_numeric,
            "total_issues": len(problems),
            "issues": problems
        }