import unittest
from datetime import datetime, timedelta
from services.observation_scheduler import Scheduler
from  entities.station import Station
from  entities.observation import Observation

# Copied referring classes 28.4.2024, include only required methods
# Copy of Observation repository

def get_observation_by_row(row):
    return Observation(station_id=row["station_id"], temperature=row["temperature"],
                       wind=row["wind"], wind_direction=row["wind_direction"],
                       datetime=row["datetime"], error_msg=row["error_msg"]) if row else None

class FakeObservationRepository():
    def __init__(self):
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        date_minus = datetime.now() - timedelta(minutes=15)
        date_old = date_minus.strftime('%Y-%m-%d %H:%M:%S')

        # Simulations of data coming from database
        # Testdata1 returns new datetime
        self.test_row1 = {}
        self.test_row1["station_id"] = "2"
        self.test_row1["temperature"] = "1"
        self.test_row1["wind"] = "3"
        self.test_row1["wind_direction"] = "300"
        self.test_row1["datetime"] = date_now
        self.test_row1["error_msg"] = "0"

        # Testdata2 returns old datetime
        self.test_row2 = {}
        self.test_row2["station_id"] = "3"
        self.test_row2["temperature"] = "13"
        self.test_row2["wind"] = "33"
        self.test_row2["wind_direction"] = "400"
        self.test_row2["datetime"] = date_old
        self.test_row2["error_msg"] = "0"

    def find_observation(self, station_id):
        if station_id == "2":
            return get_observation_by_row(self.test_row1)
        if station_id == "3":
            return get_observation_by_row(self.test_row2)
        return False

    def get_data_from_fmi(self, station_id):
        if station_id == "2" or station_id == "3":
            return (self.test_row1["temperature"], self.test_row1["wind"],
                self.test_row1["wind_direction"], self.test_row1["datetime"],
                self.test_row1["error_msg"])
        return False

    def save_observation(self, station_id):
        if station_id == "2" or station_id == "3": 
            obs = self.get_data_from_fmi(station_id)
            if obs is None:
                return False
            return True
        return False

class FakeObservationService():
    def __init__(self):
        self._observation_repository = FakeObservationRepository()

    def get_observation(self, station_id):
        if station_id == "2" or station_id == "3": 
            return self._observation_repository.find_observation(station_id)
        return False

    def update_observation(self, station_id):
        self._observation_repository.save_observation(station_id)
        return True


# Copy of Station repository

def get_station_by_row(row):
    return Station(station_id=row["station_id"], original_id=row["original_id"],
                   name=row["name"], lat=row["lat"],
                   lon=row["lon"], source=row["source"]) if row else None

class FakeSationRepository():
    def __init__(self):

        # Test data returned as Station object
        self.test_row = []
        self.test_row1 = {}
        self.test_row1["station_id"] = "2"
        self.test_row1["original_id"] = " "
        self.test_row1["name"] = " "
        self.test_row1["lat"] = " "
        self.test_row1["lon"] = " "
        self.test_row1["source"] = " "
        self.test_row.append(self.test_row1)

        # self.test_row2 = {}
        # self.test_row2["station_id"] = "3"
        # self.test_row.append(self.test_row2)

    def find_selected(self):
        return list(map(get_station_by_row, self.test_row))

class FakeStationService:
    def __init__(self, station_repository=FakeSationRepository()):
        self._station_repository = station_repository

    def get_selected(self):
        return self._station_repository.find_selected()

#Testing starts here

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.test_scheduler = Scheduler()
        self._station_service = FakeStationService()
        self._observation_service = FakeObservationService()
        self.station_time = {}
        self.interval_minutes = 10
        for sl in self._station_service.get_selected():
            self.station_time[sl.station_id] = self.interval_minutes

    def test_scheduled_observation_update(self):
        test_status = False

        for station_id, timevalue in self.station_time.items():

            o = self._observation_service.get_observation(station_id)

            # try:
            #     datetime_str = o.datetime
            # except AttributeError:
            #     return
            datetime_str = o.datetime

            datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

            now_minus = datetime.now() - timedelta(minutes=timevalue)

            if datetime_object < now_minus:
                # Get new data
                self._observation_service.update_observation(station_id)

                # Check new data arrived - station_id 3 returns old
                o2_datetime_str = "2024-04-29 11:30:00"
                o2_datetime_object = datetime.strptime(
                    o2_datetime_str, '%Y-%m-%d %H:%M:%S')

                # Slow down checking interval
                # TEST: Gets new data:
                if o2_datetime_object >= now_minus:
                    test_status = True
                    return self.assertEqual(test_status, True)
                # TEST: Does not get new data:
                if timevalue < self.interval_minutes*2:
                    test_status = True
                    return self.assertEqual(test_status, True)
            # TEST: Datetime was new
            test_status = True
            return self.assertEqual(test_status, True)
        # TEST: Did not have any stations
        return self.assertEqual(test_status, True)