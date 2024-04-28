from datetime import datetime
from entities.station import Station
from database_connection import get_database_connection


def get_station_by_row(row):
    return Station(station_id=row["station_id"], original_id=row["original_id"],
                   name=row["name"], lat=row["lat"],
                   lon=row["lon"], source=row["source"]) if row else None

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

        cursor.execute("SELECT s1.station_id, \
                       s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from stations as s1")

        rows = cursor.fetchall()

        return list(map(get_station_by_row, rows))


    def count_selected_stations(self):
        """ Counts how many selected stations are in the database.
        Returns: 
            Amount of stations
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT count(*) from selected_stations")

        row = cursor.fetchone()

        return row[0]

    def delete_selected_stations_from_database(self):
        """ Removes content from the selected_stations and observations table."""

        cursor1 = self._connection.cursor()

        cursor1.execute("delete from selected_stations")

        cursor2 = self._connection.cursor()

        cursor2.execute("delete from observations")

        self._connection.commit()
        return True

    def save_selected_station_to_database(self, station_id):
        """ Saves selected station to the database.
        Args:
        station_id: id of the selected station
        connection: Connection-object for the database"""

        cursor1 = self._connection.cursor()

        # Check if station is already saved
        try:
            cursor1.execute("SELECT station_id from selected_stations \
                            where station_id=?", (str(station_id),))
            row1 = cursor1.fetchone()
            self._connection.commit()
            if row1[0] == station_id:
                return True
        except TypeError:
            pass
        cursor = self._connection.cursor()
        date = datetime.now()
        date_str = date.strftime('%d.%m.%Y %H:%M:%S')
        cursor.execute(
            '''insert into selected_stations (station_id, temperature, wind, datetime) 
                values (?, ?, ?, ?)''',
            (str(station_id), 1, 1, str(date_str))
        )
        self._connection.commit()
        return True

    def save_nickname_to_database(self, station_id, nickname):
        """ Saves selected nickname of the selected station to the database.
        Args:
        station_id: id of the selected station
        nickname: user input
        connection: Connection-object for the database"""

        cursor1 = self._connection.cursor()

        # Check if station is saved
        try:
            cursor1.execute("SELECT station_id from selected_stations \
                            where station_id=?", (str(station_id),))
            row1 = cursor1.fetchone()
            self._connection.commit()
            if row1[0] != station_id:
                return True
        except TypeError:
            return

        cursor = self._connection.cursor()

        cursor.execute(
            '''UPDATE selected_stations SET nickname=?
                WHERE station_id=?''',
            (str(nickname), str(station_id))
        )
        self._connection.commit()
        return True

    def find_selected(self):
        """ Returns selected station from the database.
        Returns:
            list of Stations objects."""

        cursor = self._connection.cursor()

        cursor.execute("SELECT s1.station_id, s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from selected_stations as s2, stations as s1 \
                       where s1.station_id=s2.station_id")

        row = cursor.fetchall()

        return list(map(get_station_by_row, row))

    def find_station(self, station_id):
        """ Returns the object of the station.
        Args:
        station_id: id of the station"""

        cursor = self._connection.cursor()

        cursor.execute("SELECT s1.station_id, s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from stations as s1 where s1.station_id=?", (str(station_id),))

        row = cursor.fetchall()

        return list(map(get_station_by_row, row))

    def find_nickname(self, station_id):
        """ Returns the nickname of the station.
        Args:
        station_id: id of the station"""

        cursor = self._connection.cursor()

        cursor.execute("SELECT nickname \
                       from selected_stations \
                       where station_id=?", (str(station_id),))

        row = cursor.fetchone()

        nick = row[0]

        cursor1 = self._connection.cursor()

        cursor1.execute("SELECT s1.station_id, s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from stations as s1 where s1.station_id=?", (str(station_id),))

        row1 = cursor1.fetchall()

        station = list(map(get_station_by_row, row1))[0]
        station.set_nickname(nick)
        return station

    def find_error(self, station_id):
        """ Returns the errorstate of the station.
        Args:
        station_id: id of the station"""

        cursor = self._connection.cursor()

        cursor.execute("SELECT error_msg \
                       from selected_stations \
                       where station_id=?", (str(station_id),))

        row = cursor.fetchone()

        error_msg = row[0]

        cursor1 = self._connection.cursor()

        cursor1.execute("SELECT s1.station_id, s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from stations as s1 where s1.station_id=?", (str(station_id),))

        row1 = cursor1.fetchall()

        station = list(map(get_station_by_row, row1))[0]
        station.set_error_msg(error_msg)
        return station

    def delete_all(self):
        """Removes all stations from stations table.
        """

        cursor = self._connection.cursor()

        cursor.execute("delete from stations")

        self._connection.commit()


station_repository = StationRepository(get_database_connection())
