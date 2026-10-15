from pathlib import Path
from typing import Optional
import typer
from rich import print
from rich.console import Console
from rich.table import Table

from files_convertion_pipeline.core.converters import (
    CsvToExcelConverter,
    ExcelToCsvConverter,
    XmlConverter,
    TxtToExcelConverter,
)
from files_convertion_pipeline.core.validators import DataValidator

app = typer.Typer(
    name="files-convertion",
    help="CLI para la conversión y procesamiento automatizado de archivos tabulares.",
    add_completion=False,
)
console = Console()


@app.callback()
def main():
    """Pipeline de conversión de archivos (CSV, Excel, XML, TXT)."""
    pass


@app.command()
def info():
    """Muestra información y estado del pipeline."""
    print(
        "[bold green]✅ Files Convertion Pipeline CLI activo y listo para procesar.[/bold green]"
    )


@app.command()
def csv2excel(
    input_path: Path = typer.Option(
        ..., "--input", "-i", help="Ruta del archivo o carpeta CSV"
    ),
    output_path: Path = typer.Option(
        ..., "--output", "-o", help="Ruta del archivo o carpeta Excel de salida"
    ),
    unified: bool = typer.Option(
        False,
        "--unified",
        "-u",
        help="Si es un directorio, junta los CSV en un solo libro Excel con hojas separadas",
    ),
):
    """Convierte archivos CSV a Excel (.xlsx)."""
    try:
        converter = CsvToExcelConverter()
        result = converter.convert(
            input_path, output_path, unified=unified
        )
        print(
            f"[bold green]✅ Conversión completada exitosamente:[/bold green] {result}"
        )
    except Exception as e:
        print(f"[bold red]❌ Error durante la conversión:[/bold red] {e}")


@app.command()
def excel2csv(
    input_path: Path = typer.Option(
        ..., "--input", "-i", help="Ruta del archivo Excel (.xlsx/.xls)"
    ),
    output_path: Path = typer.Option(
        ..., "--output", "-o", help="Carpeta de destino para los archivos CSV"
    ),
):
    """Exporta las hojas de un libro Excel a archivos CSV individuales."""
    try:
        converter = ExcelToCsvConverter()
        result = converter.convert(input_path, output_path)
        print(
            f"[bold green]✅ Hojas exportadas exitosamente en:[/bold green] {result}"
        )
    except Exception as e:
        print(f"[bold red]❌ Error durante la conversión:[/bold red] {e}")


@app.command()
def xml2data(
    input_path: Path = typer.Option(
        ..., "--input", "-i", help="Ruta del archivo XML"
    ),
    output_path: Path = typer.Option(
        ..., "--output", "-o", help="Ruta del archivo de salida (.csv o .xlsx)"
    ),
    format: str = typer.Option(
        "csv", "--format", "-f", help="Formato de salida: 'csv' o 'excel'"
    ),
):
    """Convierte archivos XML a CSV o Excel."""
    try:
        converter = XmlConverter()
        result = converter.convert(
            input_path, output_path, target_format=format
        )
        print(
            f"[bold green]✅ Archivo XML convertido exitosamente:[/bold green] {result}"
        )
    except Exception as e:
        print(f"[bold red]❌ Error durante la conversión:[/bold red] {e}")


@app.command()
def txt2excel(
    input_path: Path = typer.Option(
        ..., "--input", "-i", help="Ruta del archivo o carpeta TXT"
    ),
    output_path: Path = typer.Option(
        ..., "--output", "-o", help="Ruta del archivo o carpeta Excel de salida"
    ),
):
    """Convierte archivos TXT a Excel (.xlsx)."""
    try:
        converter = TxtToExcelConverter()
        result = converter.convert(input_path, output_path)
        print(
            f"[bold green]✅ Conversión TXT a Excel exitosa:[/bold green] {result}"
        )
    except Exception as e:
        print(f"[bold red]❌ Error durante la conversión:[/bold red] {e}")


@app.command()
def validate(
    file_path: Path = typer.Option(
        ..., "--file", "-f", help="Ruta del archivo a inspeccionar (CSV/Excel/TXT)"
    )
):
    """Diagnostica errores de tipo o formato en columnas numéricas de un dataset."""
    try:
        report = DataValidator.inspect_numeric_columns(file_path)
        if report["total_issues"] == 0:
            print(
                "[bold green]✅ No se encontraron problemas. Todas las columnas numéricas están limpias.[/bold green]"
            )
        else:
            print(
                f"[bold yellow]⚠️ Se encontraron {report['total_issues']} error(es) en {report['file']}:[/bold yellow]"
            )
            table = Table(title="Detalle de Inconsistencias")
            table.add_column("Columna", style="cyan")
            table.add_column("Fila Excel/CSV", style="magenta")
            table.add_column("Valor Erróneo", style="red")

            for issue in report["issues"]:
                table.add_row(
                    issue["column"], str(issue["row"]), repr(issue["value"])
                )

            console.print(table)
    except Exception as e:
        print(f"[bold red]❌ Error durante el diagnóstico:[/bold red] {e}")


if __name__ == "__main__":
    app()