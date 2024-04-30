import unittest
from entities.station import Station

class TestStationService(unittest.TestCase):
    def setUp(self):
        self._station = Station(station_id="4", original_id="444", name="Test4",
                 lat="14", lon="24", source="Source4")

    def test_set_nickname(self):
        return self.assertEqual(self._station.set_nickname("Nick5"), True)

    def test_get_nickname(self):
        self._station.set_nickname("Somename4")
        return self.assertEqual(self._station.get_nickname(), "Somename4")

    def test_set_error_msg(self):
        return self.assertEqual(self._station.set_error_msg("1"), True)

    def test_get_error_msg(self):
        self._station.set_error_msg("Error4")
        return self.assertEqual(self._station.get_error_msg(), "Error4")
