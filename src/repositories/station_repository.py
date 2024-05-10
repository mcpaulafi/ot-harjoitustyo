from datetime import datetime
from entities.station import Station
from database_connection import get_database_connection

# TODO add if_station

def get_station_by_row(row):
    """Funtion returns Station objects from database result.
    Args: 
        row: contains a library
    Returns:
        Station object"""

    return Station(station_id=row["station_id"], original_id=row["original_id"],
                   name=row["name"], lat=row["lat"],
                   lon=row["lon"], source=row["source"]) if row else None

class StationRepository:
    """Class for Station operations.
    Attributes:
        connection: object which contains database connection
    """

    def __init__(self, connection):
        """Class constructor which creates a new station.

        Args:
            connection: mandatory, database connection object
        """
        self._connection = connection

    def count_all_db(self):
        """Function counts how many stations are in the database.

        Returns: 
            Amount of stations string.
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT count(*) from stations")

        row = cursor.fetchone()

        if row:
            number = row
            self._connection.commit()
            return number
        return None

    def find_all(self):
        """Returns all stations from the database.

        Returns:
            Station objects as a list.
        """
        cursor = self._connection.cursor()

        cursor.execute("SELECT s1.station_id, \
                       s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from stations as s1")

        rows = cursor.fetchall()
        self._connection.commit()

        return list(map(get_station_by_row, rows))

    def check_if_station_in_database(self, station_id):
        """Function checks if station is in the database.

        Returns:
            True if station is found
            False if not"""

        cursor1 = self._connection.cursor()
        try:
            cursor1.execute("SELECT station_id from stations \
                            where station_id=?", (str(station_id),))
            check1 = cursor1.fetchone()
            self._connection.commit()
            if check1 is None:
                return False
            return True
        except TypeError:
            return False

    def check_if_selected_in_database(self, station_id):
        """Function checks if selected station is in the database.

        Returns:
            True if station is found
            False if not"""
        try:
            cursor1 = self._connection.cursor()
            cursor1.execute("SELECT station_id from selected_stations \
                            where station_id=?", (str(station_id),))
            check = cursor1.fetchone()
            self._connection.commit()
            if check is None:
                return False
            return True
        except TypeError:
            return False

    def delete_all_db(self):
        """Removes all stations from stations table.

        Returns:
            True.
                """

        cursor = self._connection.cursor()

        cursor.execute("delete from stations")

        self._connection.commit()
        return True

    def count_selected_stations(self):
        """ Counts how many selected stations are in the database.

        Returns: 
            Amount of stations as string.
        """

        cursor = self._connection.cursor()

        cursor.execute("SELECT count(*) from selected_stations")

        row = cursor.fetchone()

        if row:
            number = row
            self._connection.commit()
            return number
        return None

    def delete_selected_stations_from_database(self):
        """ Removes content from the selected_stations and observations table.

        Returns:
            True.
        """

        cursor1 = self._connection.cursor()

        cursor1.execute("delete from selected_stations")

        cursor2 = self._connection.cursor()

        cursor2.execute("delete from observations")

        self._connection.commit()

        return True

    def save_selected_station_to_database(self, station_id):
        """ Saves selected station to the database.
        Checks if station_id alread is in the database.

        Args:
            station_id: id of the selected station
        Returns:
            True if done
            False if station not at all in database and
                    selected station already is in the database"""

        check1 = self.check_if_station_in_database(station_id)
        check2 = self.check_if_selected_in_database(station_id)

        if check1 and not check2:
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
        return False

    def save_nickname_to_database(self, station_id, nickname):
        """ Saves selected nickname of the selected station to the database.
        Checks if station is selected in the database.

        Args:
            station_id: id of the selected station
            nickname: user input

        Returns:
            True if nickname saved
            False if selected station is not in the database
        """

        if self.check_if_selected_in_database(station_id):
            cursor = self._connection.cursor()

            cursor.execute(
                '''UPDATE selected_stations SET nickname=?
                    WHERE station_id=?''',
                (str(nickname), str(station_id))
            )
            self._connection.commit()
            return True
        return False

    def find_selected(self):
        """ Returns selected stations from the database.
        Returns:
            list of Station objects."""

        cursor = self._connection.cursor()

        cursor.execute("SELECT s1.station_id, s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from selected_stations as s2, stations as s1 \
                       where s1.station_id=s2.station_id")

        row = cursor.fetchall()
        self._connection.commit()
        return list(map(get_station_by_row, row))

    def find_station(self, station_id):
        """ Function gets stations from the database and returns Station objects.

        Args:
            station_id: id of the station
            
        Returns:
            List of Station objects
            """

        cursor = self._connection.cursor()
        # TODO station not found

        cursor.execute("SELECT s1.station_id, s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from stations as s1 where s1.station_id=?", (str(station_id),))

        row = cursor.fetchone()
        self._connection.commit()
        return get_station_by_row(row)

    def get_nickname(self, station_id):
        """ Returns the nickname of the station.
        Args:
        station_id: id of the station
        Returns:
            nickname as a string"""
        cursor = self._connection.cursor()

        cursor.execute("SELECT nickname \
                       from selected_stations \
                       where station_id=?", (str(station_id),))
        row = cursor.fetchone()
        if row:
            nickname = row
            self._connection.commit()
            return nickname
        return None

    def find_nickname(self, station_id):
        """ Returns Station object with a nickname.
        Args:
        station_id: id of the station
        Returns:
            Station object"""
        nick = self.get_nickname(station_id)
        station = self.find_station(station_id)
        station.set_nickname(nick)
        return station

    def get_error(self, station_id):
        """ Returns the error state of the station.
        Args:
        station_id: id of the station
        Returns:
            Error as a string"""

        cursor = self._connection.cursor()

        cursor.execute("SELECT error_msg \
                       from selected_stations \
                       where station_id=?", (str(station_id),))

        row = cursor.fetchone()

        if row:
            error_msg = row
            self._connection.commit()
            return error_msg
        return None

    def find_error(self, station_id):
        """ Returns the Station object with an error state.
        Args:
        station_id: id of the station
        Returns:
            Station object"""

        error_msg = self.get_error(station_id)

        cursor1 = self._connection.cursor()

        cursor1.execute("SELECT s1.station_id, s1.original_id, s1.name,\
                       s1.lat, s1.lon, s1.source \
                       from stations as s1 where s1.station_id=?", (str(station_id),))

        row1 = cursor1.fetchone()

        station = get_station_by_row(row1)
        station.set_error_msg(error_msg)
        return station


station_repository = StationRepository(get_database_connection())
