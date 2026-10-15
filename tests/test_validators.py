import pandas as pd
from pathlib import Path
from files_convertion_pipeline.core.validators import DataValidator


def test_inspect_numeric_columns_with_errors(tmp_path: Path):
    # Crear un CSV con un error tipográfico en una columna numérica ('speed')
    csv_file = tmp_path / "trackmate_sample.csv"
    csv_file.write_text("speed,td\n12.5,100\n14.2,ERROR_VAL\n15.1,300")

    report = DataValidator.inspect_numeric_columns(csv_file)

    assert report["total_issues"] == 1
    assert report["issues"][0]["column"] == "td"
    assert report["issues"][0]["row"] == 3  # Fila 3 en el archivo (encabezado + 2 filas)
    assert report["issues"][0]["value"] == "ERROR_VAL"