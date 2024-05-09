from datetime import datetime, timedelta
import datetime as dt
import pytz
from fmiopendata.wfs import download_stored_query
from services.station_service import station_service
from entities.observation import Observation
from database_connection import get_database_connection


def get_observation_by_row(row):
    """Function converts database result and returns it as Observation object.
    Args: 
        row: contains a library
    Returns:
        Observation object"""
    return Observation(station_id=row["station_id"], temperature=row["temperature"],
                       wind=row["wind"], wind_direction=row["wind_direction"],
                       datetime=row["datetime"], error_msg=row["error_msg"]) if row else None


class ObservationRepository:
    """Class for Observation operations.
    """

    def __init__(self, connection):
        """Class constructor.
        Args:
            connection: Database connection object
        """
        self._connection = connection

    def get_data_from_fmi(self, station_id):
        """ Gets data for the station from FMI interphase. 
        At FMI data is stored in a coordinate (lat,lon) squares = bounding boxes.
        Stations provide new data every 1-10 minutes. 
        Timezone is UTC which is converted in return to local time.
        Request to FMI includes: 
            bounding box around the coordinates of a station.
        Reply is filtered:
            leatest timestamp (contains latest hour)
            station name
        Args:
            station_id
        Returns:
            tuple (temperature, wind, wind_direction, date, error_message)
        """
        if not station_service.get_station(station_id):
            return False

        station_lat = 0
        station_lon = 0
        station_name = ""
        for s in station_service.get_station(station_id):
            station_lat = s.lat
            station_lon = s.lon
            station_name = s.name
        extra = 0.2

        station_box = f"{str(float(station_lon)-extra)},{str(float(station_lat)-extra)},\
        {str(float(station_lon)+extra)},{str(float(station_lat)+extra)}"

        obs2 = download_stored_query("fmi::observations::weather::multipointcoverage",
                              args=[f"bbox={station_box}","timeseries=True"])

        get_error = 0
        try:
            utc_datetime = str(obs2.data[station_name]['times'][-1])
            utc_format = "%Y-%m-%d %H:%M:%S"
            local_tz = pytz.timezone('Europe/Helsinki')

            utc_dt = dt.datetime.strptime(utc_datetime, utc_format)
            local_dt = str(utc_dt.replace(
                tzinfo=pytz.utc).astimezone(local_tz))[:-6]
        except KeyError:
            print("Following station not found. No data retrieved.")
            utc_datetime = None
            local_dt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            get_error = 1

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

    def save_observation(self, station_id):
        """ Saves observation to the database. Checks if 
        in the database there is already new data.
        Args:
            station_id: id of the selected station
            """
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
        """Removes all observations from observations table.
        Returns: 
            True if no errors.
                """

        cursor = self._connection.cursor()

        cursor.execute("delete from observations")

        self._connection.commit()
        return True


observation_repository = ObservationRepository(get_database_connection())

