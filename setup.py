import os
import sys
from PyInstaller.__main__ import run

# Ruta del archivo principal de tu proyecto
main_script = "main.py"

# Ruta del icono que quieres usar
icono = os.path.abspath("logo_sr.ico")  # Usa una ruta absoluta

# Verifica si tkinterdnd2 está instalado y obtiene su ruta
try:
    import tkinterdnd2
    tkinterdnd2_path = os.path.dirname(tkinterdnd2.__file__)
except ImportError:
    tkinterdnd2_path = None
    print("Advertencia: tkinterdnd2 no está instalado. ¡Verifica esto antes de compilar!")

# Opciones de PyInstaller
options = [
    main_script,
    "--onefile",
    "--windowed",
    f"--icon={icono}",
    "--name=SynCatalog Ferrando",
    f"--add-data=logo_sr.ico;.",
]

# Añade tkinterdnd2 como recurso adicional si se encontró
if tkinterdnd2_path:
    options.append(f"--add-data={tkinterdnd2_path};tkinterdnd2")

# Función para la compilación
if sys.platform.startswith("win"):
    # Configuración adicional para Windows
    os.environ["PYINSTALLER_CONFIG_DIR"] = os.path.join(
        os.path.dirname(sys.executable), "PyInstaller"
    )
    run(options)
    print("Compilación finalizada. Puedes encontrar el ejecutable en la carpeta dist.")
else:
    print("Lo siento, esta funcionalidad solo está disponible en Windows por ahora.")
