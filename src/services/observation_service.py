from repositories.observation_repository import (
    observation_repository as default_observation_repository
)


class ObservationService:
    def __init__(
        self,
        observation_repository=default_observation_repository
    ):
        """Class constructor. Creates new service responsible for app logic.

        Args:
            station_repository:
                Optional, default ObservationRepository object.
                Object has ObservationRepository class methods.
        """
        self._observation_repository = observation_repository

    def get_observation(self, station_id):
        """Gets Observation data and returns object.

            Returns:
            Observation object.
        """
        return self._observation_repository.find_observation(station_id)

    def update_observation(self, station_id):
        """Gets and updates latest observations to the database.

            Returns:
            True.
        """
        return self._observation_repository.save_observation(station_id)

    def check_obs_if_old(self, given_date, timevalue=10):
        """Checks if date is older timevalue minutes.
        Args:
            given_date as string
            timevalue minutes as integer
        Returns:
            True if old.
            False if new.
        """
        return self._observation_repository.check_if_old(given_date, timevalue)

    def delete_observations_from_database(self):
        """Deletes all observations on the database.
        Returns:
            True.
        """
        self._observation_repository.delete_all()
        return True

observation_service = ObservationService()
