import unittest
from unittest.mock import MagicMock
from services.observation_service import ObservationService
from repositories.observation_repository import ObservationRepository
from entities.observation import Observation

class TestObservationService(unittest.TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self._observation_repository = ObservationRepository(self.connection)
        self._observation_service = ObservationService(self._observation_repository)
        self.test_row = {"station_id":"3", "temperature":"20",
                       "wind":"12", "wind_direction":"200",
                       "datetime":"2024-05-10 12:00:00", "error_msg":"0"}
        self.test_obs = Observation(station_id="1", temperature="10",
                       wind="10", wind_direction="100",
                       datetime="2024-05-10 12:10:00", error_msg="0")
        self.test_date = "2024-05-10 12:00:00"
        self.test_wind = 0
        self.test_station_id = 1
        self.fake_station_id = 999

    def test_update_observation(self):
        result = self._observation_service.update_observation(
            self.test_station_id)
        self.assertEqual(result, True)

    def test_update_observation_no_station_id(self):
        result = self._observation_service.update_observation(self.fake_station_id)
        self.assertEqual(result, False)

    def test_get_observation(self):
        self._observation_repository.find_observation = MagicMock(return_value=self.test_obs)
        result = self._observation_service.get_observation(self.test_station_id)
        self.assertIsInstance(result, Observation)
        self.assertEqual(result.wind, "10")

    def test_check_obs_if_old(self):
        self._observation_repository.check_if_old = MagicMock(return_value=True)
        result = self._observation_service.check_obs_if_old(self.test_date, 10)
        self.assertTrue(result)

    def test_check_obs_if_not(self):
        self._observation_repository.check_if_old = MagicMock(return_value=False)
        result = self._observation_service.check_obs_if_old(self.test_date, 10)
        self.assertFalse(result)

    def test_delete_observations_from_database(self):
        self._observation_repository.delete_all = MagicMock(return_value=True)
        result = self._observation_repository.delete_all()
        self.assertEqual(result, True)
