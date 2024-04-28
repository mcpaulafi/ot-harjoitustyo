from datetime import datetime, timedelta
from services.station_service import station_service
from services.observation_service import observation_service


class Scheduler:
    """Weather from the station view."""

    def __init__(self):
        """Class constructor. Retrieves new observations.

        Args:
        """
        self._frame = None
        self.station_time = {}
        self.interval_minutes = 10
        for sl in station_service.get_selected():
            self.station_time[sl.station_id] = self.interval_minutes

    def scheduled_observation_update(self):
        """ Check if time of observations is older than 10 minutes.
         Otherwise update new. If new data is not available slow down checking."""
        for station_id, timevalue in self.station_time.items():

            o = observation_service.get_observation(station_id)

            try:
                datetime_str = o.datetime
            except AttributeError:
                return

            datetime_object = datetime.strptime(
                datetime_str, '%Y-%m-%d %H:%M:%S')

            now_minus = datetime.now() - timedelta(minutes=timevalue)

            if datetime_object < now_minus:
                # Get new data
                observation_service.update_observation(station_id)

                # Check new data arrived
                o2_datetime_str = observation_service.get_observation(
                    station_id).datetime
                o2_datetime_object = datetime.strptime(
                    o2_datetime_str, '%Y-%m-%d %H:%M:%S')

                # Slow down checking interval
                if o2_datetime_object >= now_minus:
                    self.station_time[station_id] = self.interval_minutes
                    continue
                if timevalue < self.interval_minutes*2:
                    self.station_time[station_id] += 2
                    continue

                print("Observations updated again", station_id)
