from datetime import datetime
from entities.station import Station
from database_connection import get_database_connection


def get_station_by_row(row):
    # print("ROW", row["station_id"], row["name"])
    return Station(station_id=row["station_id"], original_id=row["original_id"],
                   name=row["name"], nickname=row["nickname"], lat=row["lat"],
                   lon=row["lon"], source=row["source"]) if row else None

def get_selected_by_row(row):
    return (row["station_id"], row["temperature"], row["wind"])


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
        """ Counts how many stations are in the database.
        Returns: 
            Amount of stations
        """

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

    def delete_selected_stations_from_database(self):
        """ Removes content from the selected_stations table."""

        cursor = self._connection.cursor()

        cursor.execute("delete from selected_stations")

        self._connection.commit()

    def save_selected_station_to_database(self, station_id):
        """ Saves selected station to the database.
        Args:
        station_id: id of the selected station
        connection: Connection-object for the database"""

        cursor = self._connection.cursor()
        date = datetime.now()
        date_str = date.strftime('%d.%m.%Y %H:%M:%S')

        cursor.execute(
            '''insert into selected_stations (station_id, temperature, wind, datetime) 
                values (?, ?, ?, ?)''',
                (str(station_id), 1, 1, str(date_str))
            )

        self._connection.commit()


    def find_selected(self):
        """ Returns selected station from the database.
        Returns:
            station_id, temperature and wind values in a tuple."""
        
        cursor = self._connection.cursor()

        cursor.execute("SELECT station_id, temperature, wind from selected_stations")

        row = cursor.fetchall()

        return list(map(get_selected_by_row, row))


    def find_name(self, station_id):
        """ Returns the name of the station.
        Args:
        station_id: id of the selected station"""

        cursor = self._connection.cursor()

        cursor.execute("SELECT name from stations where station_id=?", (str(station_id),))

        row = cursor.fetchone()

        return row[0]


    def delete_all(self):
        """Removes all stations from stations table.
        """

        cursor = self._connection.cursor()

        cursor.execute("delete from stations")

        self._connection.commit()


station_repository = StationRepository(get_database_connection())
