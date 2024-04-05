import unittest
from entities.station import Station
from database_connection import get_database_connection

def get_station_by_row(row):
    return Station(station_id=row["station_id"], original_id=row["fmisid"], name=row["name"], 
                   nickname=row["nickname"], lat=row["lat"], lon=row["lon"], source=row["source"]) if row else None

class FakeStationRepository:
    def __init__(self, connection=get_database_connection()):
        self._connection = connection

    def find_all(self):
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

    def test_get_stations(self):
        find_all = self._station_repository.find_all()
        self.assertEqual(len(find_all), 210)
