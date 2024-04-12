from entities.station import Station
from database_connection import get_database_connection

def get_station_by_row(row):
    #print("ROW", row["station_id"], row["name"])
    return Station(station_id=row["station_id"], original_id=row["original_id"], name=row["name"], 
                   nickname=row["nickname"], lat=row["lat"], lon=row["lon"], source=row["source"]) if row else None

class StationRepository:
    """Class for Weather Station list operations.
    """
    def __init__(self, connection):
        """Class constructor.

        Args:
            connection: Database connection object
        """
        self._connection = connection

    def count_all(self):
        cursor = self._connection.cursor()

        cursor.execute("SELECT count(*) from stations")

        row = cursor.fetchone()

        return row[0]

    def find_all(self):
        """Returns all stations.

        Returns:
            Station objects.
        """

        cursor = self._connection.cursor()

        cursor.execute("select * from stations")

        rows = cursor.fetchall()


        return list(map(get_station_by_row, rows))

# TODO: Find by name? Find by id? Create new?

    def delete_all(self):
        """Removes all stations.
        """

        cursor = self._connection.cursor()

        cursor.execute("delete from stations")

        self._connection.commit()

station_repository = StationRepository(get_database_connection())