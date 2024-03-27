from pathlib import Path 
from entities.station import Station #TODO: HOW THIS WORKS?
from config import STATIONS_FILE_PATH
from database_connection import get_database_connection

class StationListRepository:
    """Class for Weather Station list operations.
    """
    def __init__(self, file_path, connection):
        """Class constructor.

        Args:
            file_path: path to station list file
            connection: Database connection object
        """
        self._file_path = file_path
        self._connection = connection

    def find_all(self):
        return self._read()

    def _ensure_file_exists(self):
        Path(self._file_path).touch()

    def _read(self):
        stations = []

        self._ensure_file_exists()

        with open(self._file_path) as file:
            for row in file:
                row = row.replace("\n", "")
                row = row.replace("\"", "")
                parts = row.split(",")

                name = parts[0]
                fmisid = parts[1]
                lat = parts[2]
                lon = parts[3]

                stations.append(
                    Station(name, fmisid, lat, lon)
                )

        return stations

    def create(self, Station):
        """Saves Station to database.

        Args:
            Station: Station as Station object.

        Returns:
            Saved station as Station object.
        """

        cursor = self._connection.cursor()

        cursor.execute(
            "insert into stations (name, nickname, fmisid, lon, lat) values (?, ?, ?, ?, ?)",
            (Station.name, Station.nickname, Station.fmisid, Station.lon, Station.lat)
        )

        self._connection.commit()

        return Station
    
    def delete_all(self):
        """Removes all stations.
        """

        cursor = self._connection.cursor()

        cursor.execute("delete from stations")

        self._connection.commit()


if __name__ == "__main__":
    pass