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
        """Returns Observation object.
            
            Returns:
            Observation object.
        """
        return self._observation_repository.find_observation(station_id)

    def update_observation(self, station_id):
        """Updates latest observations to the database.
            
            Returns:
            Observation object.
        """
        self._observation_repository.save_observation(station_id)

    def delete_observations_from_database(self):
        self._observation_repository.delete_all()

observation_service = ObservationService()

print("OBS SERVICE\n")
