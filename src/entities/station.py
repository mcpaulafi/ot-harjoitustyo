#import uuid


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

    def __init__(self, name=None, nickname=None, fmisid=None, station_id=None, lat=None, lon=None):
        """Luokan konstruktori, joka luo uuden tehtävän.

        Args:
            Same as class attributes.
        """

        self.id = station_id #or str(uuid.uuid4())
        self.fmisid = fmisid
        self.name = name
        self.nickname = nickname
        self.lat = lat
        self.lon = lon
