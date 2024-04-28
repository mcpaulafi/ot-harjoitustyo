import unittest
from services.station_service import StationService
from entities.station import Station

def get_station_by_row(row):
    return Station(station_id=row["station_id"], original_id=row["original_id"],
                   name=row["name"], lat=row["lat"],
                   lon=row["lon"], source=row["source"]) if row else None



# Copied 28.4.2024 from real

class FakeStationRepository:
    """Class for Weather Station list operations.
    """

    def __init__(self, connection=1):
        self._connection = connection
        # Fake output from database
        self.test_row = []
        self.test_row1 = {}
        self.test_row1["station_id"] = "3"
        self.test_row1["original_id"] = "100"
        self.test_row1["name"] = "test_name"
        self.test_row1["lat"] = "10"
        self.test_row1["lon"] = "20"
        self.test_row1["source"] = "testing"
        self.test_row.append(self.test_row1)

    def count_all(self):
        return 3

    def find_all(self):
        return list(map(get_station_by_row, self.test_row))

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
        return list(map(get_station_by_row, self.test_row))

    def find_station(self, station_id):
        if station_id == 1:
            return list(map(get_station_by_row, self.test_row))
        return False

    def find_nickname(self, station_id):
        if station_id == 1:
            station = list(map(get_station_by_row, self.test_row))
            station[0].set_nickname("testnick")
            return station
        return False

    def find_error(self, station_id):
        if station_id == 1:
            error_msg = 1
            station = list(map(get_station_by_row, self.test_row))
            station[0].set_error_msg(error_msg)
            return station
        return False

    def delete_all(self):
        return True


# Testing starts here

class TestStationService(unittest.TestCase):
    def setUp(self):
        self._station_service = StationService(FakeStationRepository())
        self._station_repository = FakeStationRepository()
        self.station_id = 4

    def test_get_stations(self):
        test_result = self._station_service.get_stations()
        return self.assertEqual(len(test_result), 1)

    def test_get_station(self, station_id=1):
        test_result = self._station_service.get_station(station_id)
        return self.assertEqual(test_result[0].name, "test_name")

    # Selected stations
    def test_count_selected(self):
        test_result = self._station_service.count_selected()
        return self.assertEqual(test_result, 4)

    def test_save_selected(self, station_id=4):
        self._station_repository.save_selected_station_to_database(station_id)
        return self.assertEqual(self._station_service.save_selected(station_id), True)

    def test_save_selected_nickname(self, station_id=4, nickname="Testing123"):
        return self.assertEqual(self._station_service.save_selected_nickname(
            station_id, nickname), True)

    def test_get_selected(self):
        return self.assertEqual(len(self._station_service.get_selected()), 1)

    def test_get_nickname(self, station_id=1):
        return self.assertEqual(self._station_service.get_nickname(station_id)[0].nickname, "testnick")

    def test_get_error(self, station_id=1):
        return self.assertEqual(self._station_service.get_error(station_id)[0].error_msg, 1)

    def test_delete_selected(self):
        return self.assertEqual(self._station_service.delete_selected(), True)
