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

    def get_station(self, station_id):
        """Returns Station object.

        Returns:
            Station object.
        """
        return self._station_repository.find_station(station_id)

    def count_all(self):
        """Returns number of Stations in database.

        Returns:
            Number as string.
        """
        return self._station_repository.count_all_db()

    def delete_all(self):
        self._station_repository.delete_all_db()
        return True

    # Selected stations
    def count_selected(self):
        return self._station_repository.count_selected_stations()

    def save_selected(self, station_id):
        self._station_repository.save_selected_station_to_database(station_id)
        return True

    def save_selected_nickname(self, station_id, nickname):
        self._station_repository.save_nickname_to_database(
            station_id, nickname)
        return True

    def get_selected(self):
        """Returns selected station(s).

        Returns:
            List of Station objects.
        """
        return self._station_repository.find_selected()

    def get_nickname(self, station_id):
        return self._station_repository.find_nickname(station_id)

    def get_error(self, station_id):
        return self._station_repository.find_error(station_id)

    def delete_selected(self):
        self._station_repository.delete_selected_stations_from_database()
        return True

station_service = StationService()
