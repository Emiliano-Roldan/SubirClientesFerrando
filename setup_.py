import sys
from cx_Freeze import setup, Executable

# Reemplaza 'main.py' por el nombre de tu archivo principal
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base, icon="images/logo_sr.ico", shortcut_name="Syncatalog", copyright="Copyright 2024 Emestudio LTDA. All right reserved.")]

image_files = ["images/logo_sr.ico"]
includes = ["logger", "tkinter", "connectionSQL", "sys", "load_configuration", "xml.etree.ElementTree","requests", "frame", "os", "datetime", "yaml", "threading", "PIL", "tkinterdnd2", "core", "productos", "typing", "pyodbc"]
config_files = ["config.yaml"]

# Configuración para el ejecutable
build_exe_options = {
    "includes": includes,
    "include_files": image_files + config_files,
    # Otros parámetros de configuración, si los necesitas
}

setup(
    name="Syncatalog",
    version="1.0",
    executables=executables,
    options={"build_exe": build_exe_options}
)
#python setup.py build