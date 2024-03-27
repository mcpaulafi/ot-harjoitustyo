import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

STATIONS_FILENAME = os.getenv("STATIONS_FILENAME") or "fmi_stations.csv"
STATIONS_FILE_PATH = os.path.join(dirname, "..", "data", STATIONS_FILENAME)

DATABASE_FILENAME = os.getenv("DATABASE_FILENAME") or "database.sqlite3"
DATABASE_FILE_PATH = os.path.join(dirname, "..", "data", DATABASE_FILENAME)