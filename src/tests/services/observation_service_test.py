import unittest
import datetime as dt
from services.observation_service import ObservationService
from entities.station import Station
from entities.observation import Observation


def get_observation_by_row_fake(row):
    return Observation(station_id=row["station_id"], temperature=row["temperature"],
                       wind=row["wind"], wind_direction=row["wind_direction"],
                       datetime=row["datetime"], error_msg=["error_msg"]) if row else None

# Copied 28.4.2024 from real

class FakeStationRepository:
    def __init__(self, connection=1):
        self._connection = connection

    def find_station(self, station_id):
        if station_id == 1:
            test_obj = {"station_id" : str(station_id), "temperature":None, "wind":None, 
                    "wind_direction":None, "datetime":None, "error_msg":None}
            return Station(test_obj)
        return False

class FakeStationService:
    def __init__(self,station_repository):
        self._station_repository = station_repository

    def get_station(self, station_id):
        return self._station_repository.find_station(station_id)

class FakeObservationRepository:
    def __init__(self, connection=1):
        self._connection = connection
        self._station_service = FakeStationService(FakeStationRepository())

    def get_data_from_fmi(self, station_id):
        if not self._station_service.get_station(station_id):
            return False

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
            return get_observation_by_row_fake(test_row1)
        return False

    def delete_all(self):
        return True


# Testing begins

class TestObservationService(unittest.TestCase):
    def setUp(self):
        self._observation_service = ObservationService(FakeObservationRepository())
        self._observation_repository = FakeObservationRepository()
        self.wind = 0
        self.station_id = 1

    def test_update_observation(self):
        test_save = self._observation_service.update_observation(
            self.station_id)
        return self.assertEqual(test_save, True)

    def test_update_observation_no_station_id(self):
        test_save = self._observation_service.update_observation(34444)
        return self.assertEqual(test_save, False)

    def test_get_observation(self):
        test_result = self._observation_service.get_observation(
            self.station_id)
        wind_result = int(test_result.wind)
        return self.assertEqual(wind_result, 5)

    def test_delete_observations_from_database(self):
        return self.assertEqual(self._observation_repository.delete_all(), True)
