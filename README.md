# Files Convertion Pipeline 🚀

Pipeline modular, automatizable y distribuible en Python para la conversión y validación de archivos tabulares (`CSV`, `Excel`, `XML`, `TXT`).

## 📦 Instalación

```bash
git clone [https://github.com/tu-usuario/files-convertion-pipeline.git](https://github.com/tu-usuario/files-convertion-pipeline.git)
cd "files-convertion pipeline"
pip install -e .

#Conversión de CSV a Excel

# Archivo individual
files-convertion csv2excel --input datos.csv --output datos.xlsx

# Convertir carpeta de CSVs a un único Excel con múltiples hojas
files-convertion csv2excel --input ./csv_folder --output combinado.xlsx --unified

#Conversion de excel a csv
files-convertion excel2csv --input libro.xlsx --output ./csv_exports

#Conversion de XML y txt
files-convertion xml2data --input datos.xml --output datos.csv --format csv
files-convertion txt2excel --input lote.txt --output resultado.xlsx

#Diagnostico e integridad de datos.
files-convertion validate --file dataset.csv

#Pruebas unitarias
pytest -v

