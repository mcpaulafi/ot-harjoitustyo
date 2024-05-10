import unittest
from unittest.mock import MagicMock
from repositories.observation_repository import ObservationRepository
from repositories.observation_repository import get_observation_by_row
from entities.observation import Observation

class FakeObs:
    def __init__(self):
        self.data = {
            'StationName': {
                'times': ["2024-05-10 12:00:01", "2024-05-10 12:00:02", "2024-05-10 12:00:03", "2024-05-10 12:00:04", "2024-05-10 12:00:05"],
                'Air temperature': {
                    'values': [10, 15, 20, 25, 30]
                },
                'Wind speed': {
                    'values': [5, 10, 15, 20, 25]
                },
                'Wind direction': {
                    'values': [90, 180, 270, 360, 45]
                }
            }
        }
    
class TestObservationRepository(unittest.TestCase):
    def setUp(self):
        self.connection2 = MagicMock()
        self.mock_station_service = MagicMock()
        self._observation_repository = ObservationRepository(self.connection2)
        self.station_id = 4
        self.station_name = "StationName"
        self._fake_station_id = 999
        self._fake_station_name = "FakeStation"
        self._test_obs = FakeObs()

        self._test_observation_object = Observation({"station_id" : "5", "temperature":"10",
                "wind":"5", "wind_direction":None,
                "datetime":None, "error_msg":"0"})
        self._test_row = {"station_id" : "4", "temperature":"12",
                "wind":None, "wind_direction":None,
                "datetime":None, "error_msg":None}

    def test_get_observation_by_row(self):
        return self.assertIsInstance(get_observation_by_row(self._test_row),
                                     Observation, "Not instance")

#    def get_data_from_fmi(self, station_id):

    def test_check_data_from_fmi(self):
        self._observation_repository.utc_datetime = MagicMock(return_value='2023-04-05 12:30:45')
        result = self._observation_repository.check_data_from_fmi(self._test_obs, self.station_name)
        self.assertEqual(result[0], 30)

    def test_check_data_with_utc_datetime_none(self):
        self._observation_repository.utc_datetime = MagicMock(return_value=None)
        result = self._observation_repository.check_data_from_fmi(self._test_obs, self._fake_station_name)
        self.assertIsNone(result[0])

# def check_if_old(self, given_date, timevalue):
# def check_if_same_date(self, first_date, second_date):

    def test_save_observation(self):
        cursor = self.connection2.cursor.return_value
        cursor.execute.return_value = None
        result = self._observation_repository.save_observation(self.station_id)
        self.assertEqual(result, True)

    def test_save_observation_station_not_exists(self):
        self.mock_station_service.get_station.return_value = False
        result = self._observation_repository.save_observation(self._fake_station_id)
        self.assertFalse(result)

    def test_find_observation(self):
        cursor = self.connection2.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = self._test_row
        result = self._observation_repository.find_observation(self.station_id)
        self.assertIsInstance(result, Observation)
        self.assertEqual(result.station_id, "4")

    def test_find_observation_station_not_exists(self):
        self.mock_station_service.get_station.return_value = False
        result = self._observation_repository.find_observation(self._fake_station_id)
        self.assertFalse(result)

    def test_delete_all(self):
        cursor = self.connection2.cursor.return_value
        cursor.execute.return_value = None
        cursor.fetchone.return_value = (True,)
        result = self._observation_repository.delete_all()

        self.assertTrue(result)
