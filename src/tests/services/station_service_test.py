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

        cursor.execute("select * from stations ORDER BY name ASC")

        rows = cursor.fetchall()

        return list(map(get_station_by_row, rows))

    # def delete_all(self):
    #     cursor = self._connection.cursor()
    #     cursor.execute("delete from stations")
    #     self._connection.commit()


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


        self.assertEqual(count_all, 210)