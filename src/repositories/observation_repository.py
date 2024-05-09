from datetime import datetime, timedelta
import datetime as dt
import pytz
from fmiopendata.wfs import download_stored_query
from services.station_service import station_service
from entities.observation import Observation
from database_connection import get_database_connection


def get_observation_by_row(row):
    """Function which converts database result and returns it as an Observation object.

    Args: 
        row: contains a library for object attributes
    Returns:
        Observation object"""
    
    return Observation(station_id=row["station_id"], temperature=row["temperature"],
                       wind=row["wind"], wind_direction=row["wind_direction"],
                       datetime=row["datetime"], error_msg=row["error_msg"]) if row else None


class ObservationRepository:
    """Class for operations of Observations.

    Attributes:
        connection: object which contains database connection
    """

    def __init__(self, connection):
        """Class constructor which creates a new observation.

        Args:
            connection: mandatory, database connection object
        """
        self._connection = connection

    def get_data_from_fmi(self, station_id):
        """ Method which gets observation data for the station from FMI interphase.
        At FMI data is stored in a coordinate (lat,lon) squares = bounding boxes.
        Stations provide new data every 1-10 minutes and
        query returns all data from latest hour.
        Calls for function to check data.

        Request to FMI includes: 
            bounding box around the coordinates of the station.

        Args:
            station_id: mandatory, to get parameters from the database for the query

        """
        if not station_service.get_station(station_id):
            return False

        station_lat = 0
        station_lon = 0
        station_name = ""
        s = station_service.get_station(station_id)
        if s:
            station_lat = s.lat
            station_lon = s.lon
            station_name = s.name
        extra = 0.2

        station_box = f"{str(float(station_lon)-extra)},{str(float(station_lat)-extra)},\
        {str(float(station_lon)+extra)},{str(float(station_lat)+extra)}"

        obs2 = download_stored_query("fmi::observations::weather::multipointcoverage",
                              args=[f"bbox={station_box}","timeseries=True"])

        return self.check_data_from_fmi(obs2, station_name)

    def check_data_from_fmi(self, obs2, station_name):
        """Function which checks data received from FMI.
        If no station data is retrieved, sets all as None and error_msg as 1.
        Timezone is UTC which is converted in return to local time.

        Args:
            obs2: result of query from FMI
            station_name as string

        Reply is filtered with:
            latest timestamp
            station name

        Returns:
            tuple (temperature, wind, wind_direction, date, error_message)
        """
        get_error = 0
        try:
            utc_datetime = str(obs2.data[station_name]['times'][-1])
            utc_format = "%Y-%m-%d %H:%M:%S"
            local_tz = pytz.timezone('Europe/Helsinki')

            utc_dt = dt.datetime.strptime(utc_datetime, utc_format)
            local_dt = str(utc_dt.replace(
                tzinfo=pytz.utc).astimezone(local_tz))[:-6]
        except KeyError:
            utc_datetime = None
            local_dt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            get_error = 1

        # TODO check data
        if utc_datetime is not None:
            temperature = obs2.data[station_name]['Air temperature']['values'][-1]
            wind = obs2.data[station_name]['Wind speed']['values'][-1]
            wind_direction = obs2.data[station_name]['Wind direction']['values'][-1]
        else:
            temperature = None
            wind = None
            wind_direction = None

        return (temperature, wind, wind_direction, local_dt, get_error)

    def check_if_old(self, given_date, timevalue):
        """Function checks if datetime is not older than timevalue minutes.
        Args:
            given_date
            timevalue minutes as integer
        Returns:
            True if date is old
            False if new
        """
        datetime_object = datetime.strptime(given_date, '%Y-%m-%d %H:%M:%S')
        now_minus = datetime.now() - timedelta(minutes=timevalue)

        if datetime_object < now_minus:
            return True
        return False

    def check_if_same_date(self, first_date, second_date):
        """Function checks if dates are same.
        Args:
            first_date as string
            second_date as string
        Returns:
            True if dates are same
            False if not
        """
        datetime_object1 = first_date
        datetime_object2 = second_date

        if datetime_object1 == datetime_object2:
            return True
        return False

    def save_observation(self, station_id):
        """Function retrieves new data from FMI and
        saves observation to the database.
        Checks if station_id is valid in the database.
        Does nothing if retrieved date already is in the database.

        Args:
            station_id: id of the selected station
        Returns:
            True"""

        if not station_service.get_station(station_id):
            return False

        cursor = self._connection.cursor()

        obs = self.get_data_from_fmi(station_id)

        temperature = obs[0]
        wind = obs[1]
        wind_direction = obs[2]
        date_str = obs[3]
        error_msg = obs[4]

        if error_msg:
            error_msg = 1
        else:
            error_msg = 0

        db_obs = self.find_observation(station_id)

        if not db_obs or not self.check_if_same_date(date_str, db_obs.datetime):

            cursor.execute(
                '''insert into observations (station_id, temperature, \
                    wind, wind_direction, datetime, error_msg) 
                        values (?, ?, ?, ?, ?, ?)''',
                (str(station_id), temperature, wind,
                wind_direction, str(date_str), error_msg)
            )

            self._connection.commit()
        return True


    def find_observation(self, station_id):
        """Returns latest observations for a station from the database.

            Returns:
                Observation objects.
                If station_id is not found, returns False.
            """
        if not station_service.get_station(station_id):
            return False

        try:
            cursor = self._connection.cursor()

            cursor.execute("select * from observations where station_id=? \
                        ORDER BY observation_id DESC LIMIT 1", (str(station_id),))

            row = cursor.fetchone()
            self._connection.commit()
            return get_observation_by_row(row)

        except AttributeError:
            return False

    def delete_all(self):
        """Function removes all observations from observations table.

        Returns: 
            True if no errors.
                """

        cursor = self._connection.cursor()

        cursor.execute("delete from observations")

        self._connection.commit()
        return True


observation_repository = ObservationRepository(get_database_connection())
