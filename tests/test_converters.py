import pandas as pd
from pathlib import Path
from files_convertion_pipeline.core.converters import (
    CsvToExcelConverter,
    ExcelToCsvConverter,
    TxtToExcelConverter,
    XmlConverter,
)


def test_csv_to_excel_single_file(tmp_path: Path):
    # 1. Crear archivo CSV temporal
    csv_file = tmp_path / "sample.csv"
    df_original = pd.DataFrame({"id": [1, 2], "val": ["A", "B"]})
    df_original.to_csv(csv_file, index=False)

    # 2. Ejecutar convertidor
    output_excel = tmp_path / "sample.xlsx"
    converter = CsvToExcelConverter()
    result = converter.convert(csv_file, output_excel)

    # 3. Validar
    assert result.exists()
    df_converted = pd.read_excel(result)
    assert len(df_converted) == 2
    assert list(df_converted.columns) == ["id", "val"]


def test_excel_to_csv_multisheet(tmp_path: Path):
    # 1. Crear Excel con 2 hojas
    excel_file = tmp_path / "multi.xlsx"
    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        pd.DataFrame({"a": [1]}).to_excel(writer, sheet_name="Sheet1", index=False)
        pd.DataFrame({"b": [2]}).to_excel(writer, sheet_name="Sheet2", index=False)

    # 2. Convertir
    output_dir = tmp_path / "csv_out"
    converter = ExcelToCsvConverter()
    converter.convert(excel_file, output_dir)

    # 3. Validar generación de CSVs por hoja
    assert (output_dir / "Sheet1.csv").exists()
    assert (output_dir / "Sheet2.csv").exists()


def test_txt_to_excel(tmp_path: Path):
    # 1. Crear TXT delimitado
    txt_file = tmp_path / "data.txt"
    txt_file.write_text("col1,col2\n10,20\n30,40")

    # 2. Convertir
    excel_out = tmp_path / "data.xlsx"
    converter = TxtToExcelConverter()
    result = converter.convert(txt_file, excel_out)

    # 3. Validar
    df = pd.read_excel(result)
    assert df["col1"].iloc[0] == 10