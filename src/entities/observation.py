class Observation:
    """Class for a observation

    Attributes:
        station_id: String for station id in this app.
        temperature: String for temperature.
        wind: String for wind m/s.
        wind_direction: String for wind direction in degrees.
        datetime: time of the observation
        error_msg: 1 = Station not found. No data retrieved.
    """

    def __init__(self, station_id=None, temperature=None, wind=None, wind_direction=None,
                 datetime=None, error_msg=None):
        """Class constructor, creates a new observation.

        Args:
            Same as class attributes.
        """

        self.station_id = station_id
        self.temperature = temperature
        self.wind = wind
        self.wind_direction = wind_direction
        self.datetime = datetime
        self.error_msg = error_msg
