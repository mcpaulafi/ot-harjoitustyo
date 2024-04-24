from repositories.station_repository import (
    station_repository as default_station_repository
)


class StationService:
    def __init__(
        self,
        station_repository=default_station_repository
    ):
        """Class constructor. Creates new service responsible for app logic.

        Args:
            station_repository:
                Optional, default StationRepository object.
                Object has StationRepository class methods.
        """
        self._station_repository = station_repository

    def get_stations(self):
        """Returns all stations.

        Returns:
            List of Station objects.
        """
        return self._station_repository.find_all()

    def save_selected(self, station_id):
        self._station_repository.save_selected_station_to_database(station_id)

    def delete_selected(self):
        # TODO remove obs
        self._station_repository.delete_selected_stations_from_database()
#        observation_service.delete_observations_from_database()

    def count_selected(self):
        return self._station_repository.count_selected_stations()

    def get_selected(self):
        """Returns selected station(s).

        Returns:
            List of Station objects.
        """
        return self._station_repository.find_selected()

    def get_selected_obs(self, station_id):
        """Returns measurement settings for selected station.

        Returns:
            Duple.
        """
        return self._station_repository.find_selected_obs(station_id)

    def get_name(self, station_id):
        """Returns Station object.

        Returns:
            Station object.
        """
        return self._station_repository.find_station(station_id)


station_service = StationService()
