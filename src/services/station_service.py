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


station_service = StationService()
