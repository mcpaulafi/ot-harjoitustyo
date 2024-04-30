import unittest
from unittest import mock
from unittest.mock import MagicMock
from repositories.observation_repository import ObservationRepository
from repositories.observation_repository import get_observation_by_row
from services.station_service import StationService
from entities.observation import Observation

# Testing begins

class TestObservationRepository(unittest.TestCase):
    def setUp(self):
        self.connection = mock.Mock()
        self.mock_station_service = MagicMock()
        self._observation_repository = ObservationRepository(self.connection)
        self._station_service = StationService(self.connection)
        self.station_id = 4
        self._fake_station_id = 999

        self._test_observation_object = Observation({"station_id" : "5", "temperature":"10",
                "wind":"5", "wind_direction":None,
                "datetime":None, "error_msg":"0"})
        self._test_row = {"station_id" : "4", "temperature":"12", 
                "wind":None, "wind_direction":None,
                "datetime":None, "error_msg":None}

    def test_get_observation_by_row(self):
        return self.assertIsInstance(get_observation_by_row(self._test_row), 
                                     Observation, "Not instance")

    def test_get_observation(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = self._test_row
        result = self._observation_repository.find_observation(self.station_id)
        self.assertIsInstance(result, Observation)
        self.assertEqual(result.station_id, "4")

    def test_get_observation_station_not_exists(self):
        self.mock_station_service.get_station.return_value = False
        result = self._observation_repository.find_observation(self._fake_station_id)
        self.assertFalse(result)

    def test_delete_all(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = (True,)
        result = self._observation_repository.delete_all()

        self.assertEqual(result, True)
        return True

    def test_save_observation(self):
        cursor = self.connection.cursor.return_value
        cursor.execute.return_value = None
        result = self._observation_repository.save_observation(self.station_id)
        self.assertEqual(result, True)

    def test_save_observation_station_not_exists(self):
        self.mock_station_service.get_station.return_value = False
        result = self._observation_repository.save_observation(self._fake_station_id)
        self.assertFalse(result)

 