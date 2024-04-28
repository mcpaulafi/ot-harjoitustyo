import unittest
import datetime as dt
from entities.observation import Observation


def get_observation_by_row(row):
    return Observation(station_id=row["station_id"], temperature=row["temperature"],
                       wind=row["wind"], wind_direction=row["wind_direction"],
                       datetime=row["datetime"], error_msg=["error_msg"]) if row else None

# Copied 28.4.2024 from real


class FakeObservationRepository:
    def __init__(self, connection=1):
        self._connection = connection

    def get_data_from_fmi(self, station_id):
        if station_id == 1:
            get_error = 0
            local_dt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            temperature = 12
            wind = 4
            wind_direction = 200
            return (temperature, wind, wind_direction, local_dt, get_error)
        return False

    def save_observation(self, station_id):
        if station_id == 1:
            return True
        return False

    def find_observation(self, station_id):
        if station_id == 1:
            # Fake output from database
            test_row = []
            test_row1 = {}
            test_row1["station_id"] = "1"
            test_row1["temperature"] = "10"
            test_row1["wind"] = "5"
            test_row1["wind_direction"] = "150"
            test_row1["datetime"] = "2024-04-28 12:00:01"
            test_row1["error_msg"] = 0
            test_row.append(test_row1)
            return get_observation_by_row(test_row1)
        return False

    def delete_all(self):
        return True

# Testing begins


class TestObservationService(unittest.TestCase):
    def setUp(self):
        # observation_service.delete_observations_from_database()
        self._observation_repository = FakeObservationRepository()
        self.wind = 0
        self.station_id = 1

    def test_update_observation(self):
        test_save = self._observation_repository.save_observation(
            self.station_id)
        return self.assertEqual(test_save, True)

    def test_get_observation(self):
        test_result = self._observation_repository.find_observation(
            self.station_id)
        # Why ERROR here?
        wind_result = int(test_result.wind)
        return self.assertEqual(wind_result, 5)

    def test_delete_observations_from_database(self):
        return self.assertEqual(self._observation_repository.delete_all(), True)
