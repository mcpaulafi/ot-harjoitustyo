import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from services.observation_scheduler import Scheduler
from  services.observation_service import ObservationService
from services.station_service import StationService

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.connection3 = MagicMock()
        self.test_scheduler = Scheduler()
        self._station_service = StationService(self.connection3)
        self._observation_service = ObservationService(self.connection3)
        self.station_id= 1
        self.timevalue= 10

    def test_scheduled_observation_update_false(self):
        self._observation_service.update_observation(self.station_id)

        nowtime  = datetime.now() + timedelta(minutes=20)
        self._observation_service.get_observation(self.station_id).datetime = MagicMock(return_value=
        nowtime.strftime('%Y-%m-%d %H:%M:%S'))

        result = self.test_scheduler.scheduled_observation_update(self.station_id, self.timevalue)

        return self.assertFalse(result)

    def test_scheduled_observation_update_true(self):
        self._observation_service.update_observation(self.station_id)
        now_minus1  = datetime.now() - timedelta(minutes=20)

        self._observation_service.get_observation(self.station_id).datetime = MagicMock(return_value=
        now_minus1.strftime('%Y-%m-%d %H:%M:%S'))

        result = self.test_scheduler.scheduled_observation_update(self.station_id, self.timevalue)

        return self.assertFalse(result)
