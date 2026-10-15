from abc import ABC, abstractmethod
from pathlib import Path

class BaseConverter(ABC):
    """Interfaz base para todos los convertidores de archivos del pipeline."""

    @abstractmethod
    def convert(self, input_path: Path, output_path: Path) -> Path:
        """
        Lee el archivo de entrada y lo guarda en el formato de salida deseado.
        
        :param input_path: Ruta del archivo o carpeta de origen.
        :param output_path: Ruta del archivo o carpeta de destino.
        :return: Ruta del archivo o directorio procesado.
        """
        pass