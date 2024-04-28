class Station:
    """Class for a weather station

    Attributes:
        station_id: String for station id in this app.
        fmisid: String for station id by source.
        name: String for station name by source.
        nickname: String for station name by user.
        lat: String for latitude of the station location.
        lon: String for longtitude of the station location.
    """

    def __init__(self, station_id=None, original_id=None, name=None,
                 lat=None, lon=None, source=None):
        """Class constructor, creates a new station.

        Args:
            Same as class attributes.
        """

        self.station_id = station_id
        self.original_id = original_id
        self.name = name
        self.nickname = None
        self.lat = lat
        self.lon = lon
        self.source = source
        self.error_msg = 0

    def set_nickname(self, nickname):
        """Method to set nickname.
        Args: 
        nickname"""
        self.nickname = nickname

    def get_nickname(self):
        """Method to get nickname."""
        return self.nickname

    def set_error_msg(self, error_msg):
        """Method to set nickname.
        Args: 
        nickname"""
        self.error_msg = error_msg

    def get_error_msg(self):
        """Method to get nickname."""
        return self.error_msg
