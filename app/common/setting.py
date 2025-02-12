# coding: utf-8
import sys
from pathlib import Path
from PySide6.QtCore import QStandardPaths

# change DEBUG to False if you want to compile the code to exe
DEBUG = "__compiled__" not in globals()


YEAR = 2025
AUTHOR = "zhiyiYo"
VERSION = "0.2.0"
APP_NAME = "Fluent-M3U8"
HELP_URL = "https://github.com/zhiyiYo/Fluent-M3U8"
REPO_URL = "https://github.com/zhiyiYo/Fluent-M3U8"
FEEDBACK_URL = "https://github.com/zhiyiYo/Fluent-M3U8/issues"
RELEASE_URL = "https://github.com/zhiyiYo/Fluent-M3U8/releases"
DOC_URL = "https://github.com/zhiyiYo/Fluent-M3U8/"


if DEBUG:
    CONFIG_FOLDER = Path('AppData').absolute()
else:
    CONFIG_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) / APP_NAME

CONFIG_FILE = CONFIG_FOLDER / "config.json"
DB_PATH = CONFIG_FOLDER / "database.db"

COVER_FOLDER = CONFIG_FOLDER / "Cover"
COVER_FOLDER.mkdir(exist_ok=True, parents=True)

if sys.platform == "win32":
    EXE_SUFFIX = ".exe"
else:
    EXE_SUFFIX = ""
