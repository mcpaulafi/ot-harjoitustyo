import unittest
from unittest.mock import MagicMock
from repositories.station_repository import StationRepository
from repositories.station_repository import get_station_by_row
from entities.station import Station


class TestStationRepository(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.mock_station_service = MagicMock()
        self._station_repository = StationRepository(self.connection)
        self.station_id = 4
        self._fake_station_id = 999
        self.nickname = "NickStation"

        self.test_stations = [
        Station(station_id="1", original_id="2", name="StationA", 
                lat="20.1", lon="60.1", source="Source1"),
        Station(station_id="3", original_id="4", name="StationB", 
                lat="20.2", lon="60.2", source="Source2")
    ]

        self.test_station1 = Station(station_id="4", original_id="41", name="StationD", 
                lat="20.4", lon="60.4", source="Source1")
        self.test_station1.set_nickname = self.nickname

        self.test_row1 = {"station_id": "3", "original_id": "31", 
                          "name": "Station 3",
         "lat": "20.2", "lon": "60.2", "source": "Source1"}

        self.test_rows = [
        {"station_id": "1", "original_id": "2", "name": "StationA", 
         "lat": "20.1", "lon": "60.1", "source": "Source1"},
        {"station_id": "3", "original_id": "4", "name": "StationB", 
         "lat": "20.2", "lon": "60.2", "source": "Source2"}
    ]

    def test_get_station_by_row(self):
        return self.assertIsInstance(get_station_by_row(self.test_row1),
                                     Station, "Not instance")

    def test_count_all_db(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = 3
        result = self._station_repository.count_all_db()

        self.assertEqual(result, 3)

    def test_find_all(self):
        cursor = self.connection.cursor.return_value
        cursor.fetchall.return_value = self.test_rows
        result = self._station_repository.find_all()

        self.assertEqual(len(result), len(self.test_stations))
        for i, station in enumerate(result):
            self.assertEqual(station.station_id, self.test_stations[i].station_id)

    def test_check_if_station_in_database(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = True
        result = self._station_repository.check_if_station_in_database(self.station_id)
        self.assertEqual(result, True)

    def test_check_if_station_in_database_not(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = None
        result = self._station_repository.check_if_station_in_database(self._fake_station_id)
        self.assertEqual(result, False)


    def test_check_if_selected_in_database(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = True
        result = self._station_repository.check_if_selected_in_database(self.station_id)
        self.assertEqual(result, True)

    def test_check_if_selected_in_database_not(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = None
        result = self._station_repository.check_if_selected_in_database(self._fake_station_id)
        self.assertEqual(result, False)

    def test_delete_all_db(self):
        result = self._station_repository.delete_all_db()
        self.assertTrue(result)

    def test_count_selected_stations(self):
        cursor = self.connection.cursor.return_value
        cursor.fetchone.return_value = 3
        result = self._station_repository.count_selected_stations()
        self.assertEqual(result, 3)

    def test_delete_selected_stations_from_database(self):
        result = self._station_repository.delete_selected_stations_from_database()
        self.assertTrue(result)

    def test_save_selected_station_to_database(self):
        self._station_repository.check_if_station_in_database = MagicMock(return_value=True)
        self._station_repository.check_if_selected_in_database = MagicMock(return_value=False)
        result = self._station_repository.save_selected_station_to_database(self.station_id)
        self.assertTrue(result)

    def test_save_selected_station_to_database_not(self):
        self._station_repository.check_if_station_in_database = MagicMock(return_value=False)
        self._station_repository.check_if_selected_in_database = MagicMock(return_value=False)
        result = self._station_repository.save_selected_station_to_database(self.station_id)
        self.assertFalse(result)

    def test_save_nickname_to_database(self):
        self._station_repository.check_if_selected_in_database = MagicMock(return_value=True)
        result = self._station_repository.save_nickname_to_database(self.station_id, self.nickname)
        self.assertTrue(result)

    def test_save_nickname_to_database_not(self):
        self._station_repository.check_if_selected_in_database = MagicMock(return_value=False)
        result = self._station_repository.save_nickname_to_database(self.station_id, self.nickname)
        self.assertFalse(result)

    def test_find_selected(self):
        cursor = self.connection.cursor.return_value
        cursor.fetchall.return_value = self.test_rows
        result = self._station_repository.find_selected()

        self.assertEqual(len(result), len(self.test_stations))
        for i, station in enumerate(result):
            self.assertEqual(station.station_id, self.test_stations[i].station_id)

    def test_find_station(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = self.test_row1
        result = self._station_repository.find_station(self.station_id)
        self.assertIsInstance(result, Station)
        self.assertEqual(result.station_id, "3")

    def test_get_nickname(self):
        cursor = self.connection.cursor.return_value
        cursor.fetchone.return_value = self.nickname
        result = self._station_repository.get_nickname(self.station_id)
        self.assertEqual(result, "NickStation")

    def test_get_nickname_not(self):
        cursor = self.connection.cursor.return_value
        cursor.fetchone.return_value = None
        result = self._station_repository.get_nickname(self.station_id)
        self.assertFalse(result)

    def test_find_nickname(self):
        self._station_repository.get_nickname = MagicMock(return_value=self.nickname)
        cursor = self.connection.cursor.return_value
        cursor.fetchone.return_value = self.test_row1
        result = self._station_repository.find_nickname(self.station_id)
        self.assertEqual(result.nickname, "NickStation")

    def test_get_error_not(self):
        cursor = self.connection.cursor.return_value
        cursor.fetchone.return_value = None
        result = self._station_repository.get_error(self.station_id)
        self.assertFalse(result)

    def test_get_error(self):
        cursor = self.connection.cursor.return_value
        cursor.fetchone.return_value = "1"
        result = self._station_repository.get_error(self.station_id)
        self.assertEqual(result, "1")

    def test_find_error(self):
        self._station_repository.get_error = MagicMock(return_value="1")
        cursor = self.connection.cursor.return_value
        cursor.fetchone.return_value = self.test_row1
        result = self._station_repository.find_error(self.station_id)
        self.assertEqual(result.error_msg, "1")