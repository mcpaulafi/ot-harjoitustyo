import unittest
from entities.station import Station

def get_station_by_row(row):
    return Station(station_id=row["station_id"], original_id=row["original_id"],
                   name=row["name"], lat=row["lat"],
                   lon=row["lon"], source=row["source"]) if row else None

# Fake output from database
test_row = []
test_row1 = {}
test_row1["station_id"] = "1"
test_row1["original_id"] = "100"
test_row1["name"] = "test_name"
test_row1["lat"] = "10"
test_row1["lon"] = "20"
test_row1["source"] = "testing"
test_row.append(test_row1)

# Copied 28.4.2024 from real

class FakeStationRepository:
    """Class for Weather Station list operations.
    """

    def __init__(self, connection=1):
        self._connection = connection

    def count_all(self):
        return 3

    def find_all(self):
        rows = ""
        return list(map(get_station_by_row, rows))

    def count_selected_stations(self):
        return 4

    def delete_selected_stations_from_database(self):
        return True

    def save_selected_station_to_database(self, station_id):
        if station_id == 4:
            return True
        return False

    def save_nickname_to_database(self, station_id, nickname):
        if station_id == 5 and nickname == "Testing123":
            return True
        return False

    def find_selected(self):
        return list(map(get_station_by_row, test_row))

    def find_station(self, station_id):
        if station_id == 1:
            return list(map(get_station_by_row, test_row))
        return False

    def find_nickname(self, station_id):
        if station_id == 1:
            station = list(map(get_station_by_row, test_row))
            station[0].set_nickname("testnick")
            return station
        return False

    def find_error(self, station_id):
        if station_id == 1:
            error_msg = 1
            station = list(map(get_station_by_row, test_row))
            station[0].set_error_msg(error_msg)
            return station
        return False

    def delete_all(self):
        return True


# Testing starts here

class TestStationService(unittest.TestCase):
    def setUp(self):
        self._station_repository = FakeStationRepository()

    def get_stations(self):
        return self.assertEqual(self._station_repository.find_all(), 3)

    def test_get_station(self, station_id=1):
        return self.assertEqual(self._station_repository.find_station(station_id)[0].name, "test_name")

    # Selected stations
    def test_count_selected(self):
        return self.assertEqual(self._station_repository.count_selected_stations(), 4)

    def test_save_selected(self, station_id=4):
        self._station_repository.save_selected_station_to_database(station_id)
        return self.assertEqual(self._station_repository.save_selected_station_to_database(station_id), True)

    def test_save_selected_nickname(self, station_id=5, nickname="Testing123"):
        return self.assertEqual(self._station_repository.save_nickname_to_database(
            station_id, nickname), True)

    def test_get_selected(self):
        return self.assertEqual(len(self._station_repository.find_selected()), 1)

    def test_get_nickname(self, station_id=1):
        return self.assertEqual(self._station_repository.find_nickname(station_id)[0].nickname, "testnick")

    def test_get_error(self, station_id=1):
        return self.assertEqual(self._station_repository.find_error(station_id)[0].error_msg, 1)

    def test_delete_selected(self):
        return self.assertEqual(self._station_repository.delete_selected_stations_from_database(), True)
