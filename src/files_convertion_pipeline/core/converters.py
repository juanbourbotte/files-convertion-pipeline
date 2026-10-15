from pathlib import Path
from typing import List, Union
import pandas as pd
from files_convertion_pipeline.core.base import BaseConverter


class CsvToExcelConverter(BaseConverter):
    """Convierte archivos CSV a Excel (.xlsx), ya sea un archivo individual,

    un directorio entero o combinándolos en un único libro con múltiples
    hojas.
    """

    def convert(
        self,
        input_path: Path,
        output_path: Path,
        unified: bool = False,
    ) -> Path:
        input_path = Path(input_path)
        output_path = Path(output_path)

        if input_path.is_file():
            df = pd.read_csv(input_path)
            df.to_excel(output_path, index=False)
            return output_path

        elif input_path.is_dir():
            csv_files = sorted(list(input_path.glob("*.csv")))
            if not csv_files:
                raise FileNotFoundError(
                    f"No se encontraron archivos CSV en {input_path}"
                )

            if unified:
                # Combinar varios CSV en un único archivo Excel con múltiples pestañas
                with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                    for csv_file in csv_files:
                        sheet_name = csv_file.stem[:31]  # Máximo 31 caracteres
                        df = pd.read_csv(csv_file)
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                return output_path
            else:
                # Convertir cada CSV a un archivo Excel individual
                output_path.mkdir(parents=True, exist_ok=True)
                for csv_file in csv_files:
                    target_file = output_path / f"{csv_file.stem}.xlsx"
                    df = pd.read_csv(csv_file)
                    df.to_excel(target_file, index=False)
                return output_path
        else:
            raise ValueError(f"La ruta de entrada no existe: {input_path}")


class ExcelToCsvConverter(BaseConverter):
    """Extrae las hojas de un libro Excel (.xlsx / .xls) y las guarda como archivos CSV independientes."""

    def convert(self, input_path: Path, output_path: Path) -> Path:
        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.is_file():
            raise FileNotFoundError(
                f"El archivo Excel especificado no existe: {input_path}"
            )

        output_path.mkdir(parents=True, exist_ok=True)
        xls = pd.ExcelFile(input_path)

        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            safe_sheet_name = sheet.replace(" ", "_").replace("/", "-")
            csv_file = output_path / f"{safe_sheet_name}.csv"
            df.to_csv(csv_file, index=False)

        return output_path


class XmlConverter(BaseConverter):
    """Convierte datos estructurados XML a formato CSV o Excel."""

    def convert(
        self, input_path: Path, output_path: Path, target_format: str = "csv"
    ) -> Path:
        input_path = Path(input_path)
        output_path = Path(output_path)

        if not input_path.is_file():
            raise FileNotFoundError(
                f"El archivo XML especificado no existe: {input_path}"
            )

        df = pd.read_xml(input_path)

        if target_format.lower() == "csv":
            df.to_csv(output_path, index=False)
        elif target_format.lower() in ["excel", "xlsx"]:
            df.to_excel(output_path, index=False)
        else:
            raise ValueError(
                f"Formato no soportado para XML: {target_format}. Usa 'csv' o 'excel'."
            )

        return output_path


class TxtToExcelConverter(BaseConverter):
    """Convierte archivos de texto (.txt) con delimitadores detectados automáticamente a Excel."""

    def convert(self, input_path: Path, output_path: Path) -> Path:
        input_path = Path(input_path)
        output_path = Path(output_path)

        if input_path.is_file():
            df = pd.read_csv(input_path, sep=None, engine="python")
            df.to_excel(output_path, index=False)
            return output_path
        elif input_path.is_dir():
            output_path.mkdir(parents=True, exist_ok=True)
            txt_files = list(input_path.glob("*.txt"))
            for txt_file in txt_files:
                df = pd.read_csv(txt_file, sep=None, engine="python")
                target_file = output_path / f"{txt_file.stem}.xlsx"
                df.to_excel(target_file, index=False)
            return output_path
        else:
            raise ValueError(f"Ruta no válida: {input_path}")