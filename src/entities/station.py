class Station:
    """Class for a weather station.

    Attributes:
        station_id: String for station id in this app.
        original_id: String for id used by the source.
        name: String for station name by source.
        nickname: String for station name by user.
        lat: String for latitude of the station location.
        lon: String for longtitude of the station location.
        source: String for where the station originally comes from.
        error_msg: String for error message.
    """

    def __init__(self, station_id=None, original_id=None, name=None,
                 lat=None, lon=None, source=None):
        """Class constructor, creates a new station.

        Args:
            station_id: String for station id in this app.
            original_id: String for id used by the source.
            name: String for station name by source.
            nickname: String for station name by user.
            lat: String for latitude of the station location.
            lon: String for longtitude of the station location.
            source: String for where the station originally comes from.
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
            nickname string
        Returns:
            True"""
        self.nickname = nickname
        return True

    def get_nickname(self):
        """Method to get nickname.

        Returns:
            nickname as string"""
        return self.nickname

    def set_error_msg(self, error_msg):
        """Method to set error message.

        Args: 
            error_msg as string
        Returns:
            True"""
        self.error_msg = error_msg
        return True

    def get_error_msg(self):
        """Method to get error message.

        Returns:
            error message as a string"""
        return self.error_msg
