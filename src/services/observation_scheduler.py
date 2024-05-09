from datetime import datetime, timedelta
from services.observation_service import observation_service


class Scheduler:
    """Weather from the station view."""

    def __init__(self):
        """Class constructor. Retrieves new observations.

        Args:
        """
        self._frame = None

    def scheduled_observation_update(self, station_id, timevalue):
        """ Update observation data for selected stations. 
        If new data is not available slow down checking by adding timevalue.
        Args:
            station_id 
            timevalue minutes in integer
        Returns
            True if observations are updated
            False if no new data was retrieved
        """
        observation_service.update_observation(station_id)

        o2_datetime_str = observation_service.get_observation(
                    station_id).datetime
        o2_datetime_object = datetime.strptime(
                    o2_datetime_str, '%Y-%m-%d %H:%M:%S')

        now_minus = datetime.now() - timedelta(minutes=timevalue)

        if o2_datetime_object >= now_minus:
            return True
        return False
