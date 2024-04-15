import unittest
from entities.station import Station
from database_connection import get_database_connection


def get_station_by_row(row):
    return Station(station_id=row["station_id"], original_id=row["original_id"], name=row["name"],
                   nickname=row["nickname"], lat=row["lat"], lon=row["lon"], source=row["source"]) if row else None


class FakeStationRepository:
    def __init__(self, connection=get_database_connection()):
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

    def find_station(self, station_id):
        """ Returns the object of the station.
        Args:
        station_id: id of the station"""

        cursor = self._connection.cursor()

        cursor.execute("SELECT * from stations where station_id=?", (str(station_id),))

        row = cursor.fetchall()

        return list(map(get_station_by_row, row))


class TestStationService(unittest.TestCase):
    def setUp(self):
        self._station_repository = FakeStationRepository()

    def test_count_stations(self):
        """Database should contain 210 stations"""
        count_all = self._station_repository.count_all()
        self.assertEqual(count_all, 210)

    def test_all_stations(self):
        """Check if selected station exists in the database"""
        find_all = self._station_repository.find_all()
        test_name = "Not found"
        for s in find_all:
            if s.original_id == "100996":
                test_name = s.name

        return self.assertEqual(test_name, "Helsinki Harmaja")

    def test_get_name(self):
        """Check if name is retrieved from database"""
        get_name = self._station_repository.find_station("20")
        test_name = "Not found"
        for n in get_name:
            if n.station_id == 20:
                test_name = n.name

        return self.assertEqual(test_name, "Hattula Lepaa")
