import unittest
from unittest.mock import MagicMock
from repositories.station_repository import StationRepository
from services.station_service import StationService
from entities.station import Station

class TestStationService(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self._station_repository = StationRepository(self.connection)
        self._station_service = StationService(self._station_repository)

        self.test_station1 = Station(station_id="4", original_id="41", name="StationD", 
                lat="20.4", lon="60.4", source="Source1")

        self.test_stations = [
        Station(station_id="2", original_id="22", name="StationA", 
                lat="20.1", lon="60.1", source="Source1"),
        Station(station_id="3", original_id="44", name="StationB", 
                lat="20.2", lon="60.2", source="Source2")
        ]

        self.station_id = 4
        self.fake_station_id = 999
        self.nickname = "NickStation1"
        self.test_station1.set_nickname(self.nickname)
        self.test_error = 1
        self.test_station1.set_error_msg(self.test_error)

    def test_get_stations(self):
        self._station_repository.find_all = MagicMock(return_value=10)
        result = self._station_service.get_stations()
        self.assertEqual(result, 10)

    def test_get_station(self):
        self._station_repository.find_station = MagicMock(return_value=self.test_station1)
        result = self._station_service.get_station(self.station_id)
        self.assertEqual(result.name, "StationD")

    def test_count_selected(self):
        self._station_repository.count_selected_stations = MagicMock(return_value=2)
        result = self._station_service.count_selected()
        self.assertEqual(result, 2)

    def test_save_selected(self):
        self._station_repository.check_if_station_in_database = MagicMock(return_value=True)
        self._station_repository.check_if_selected_in_database = MagicMock(return_value=False)
        result = self._station_service.save_selected(self.station_id)
        self.assertEqual(result, True)

    def test_get_selected(self):
        self._station_repository.find_selected = MagicMock(return_value=self.test_stations)
        result = self._station_service.get_selected()
        self.assertEqual(len(result), 2)

    def test_save_selected_nickname(self):
        self._station_repository.save_nickname_to_database = MagicMock(return_value=True)
        result = self._station_service.save_selected_nickname(self.station_id, self.nickname)
        self.assertTrue(result)

    def test_get_nickname(self):
        self._station_repository.find_nickname = MagicMock(return_value=self.test_station1)
        result = self._station_service.get_nickname(self.station_id)
        self.assertEqual(result.nickname,"NickStation1")

    def test_get_error(self):
        self._station_repository.find_error = MagicMock(return_value=self.test_station1)
        result = self._station_service.get_error(self.station_id)
        self.assertIsInstance(result, Station)
        self.assertEqual(result.error_msg, self.test_error)

    def test_delete_selected(self):
        self._station_repository.delete_selected_stations_from_database = MagicMock(return_value=True)
        result = self._station_service.delete_selected()
        self.assertTrue(result)

    def test_delete_all(self):
        self._station_repository.delete_all_db = MagicMock(return_value=True)
        result = self._station_service.delete_all()
        self.assertTrue(result)

    def test_count_all(self):
        self._station_repository.count_all_db = MagicMock(return_value=3)
        result = self._station_service.count_all()
        self.assertEqual(result, 3)
