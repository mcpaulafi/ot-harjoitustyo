from datetime import timezone
import datetime as dt
import pytz
from fmiopendata.wfs import download_stored_query
from services.station_service import station_service
from entities.observation import Observation
from database_connection import get_database_connection

def get_observation_by_row(row):
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

        Args:
            station_id
        Returns:
            tuple (temperature, wind, wind_direction)
        """
        station_lat = 0
        station_lon = 0
        station_name = ""
        for s in station_service.get_station(station_id):
            station_lat = s.lat
            station_lon = s.lon
            station_name = s.name
        extra = 0.2
        # ERROR Inari Seitalaassa, muitakin

        # At FMI data is stored in a coordinate squares = bounding boxes.
        # Formula for an area in which the station is located.
        # Entire Finland bbox=18.7,59.6,31.4,70.2"

        station_box = f"{str(float(station_lon)-extra)},{str(float(station_lat)-extra)},\
        {str(float(station_lon)+extra)},{str(float(station_lat)+extra)}"

        # Retrieve the latest hour of data
        end_time = dt.datetime.now(timezone.utc)
        start_time = end_time - dt.timedelta(hours=1)

        # Convert times to properly formatted strings
        start_time = start_time.isoformat(timespec="seconds") + "Z"
        end_time = end_time.isoformat(timespec="seconds") + "Z"
        # -> 2020-07-07T13:00:00Z

        # Retrievind data for the box
        obs2 = download_stored_query("fmi::observations::weather::multipointcoverage",
                                     args=[f"bbox={station_box}",
                                           "timeseries=True"])
        # All data
        # print(sorted(obs2.data.keys()))

        # The times are as a list of datetime objects, printing latest obs
        # KeyError: Station name is not found
        get_error = 0

        try:
            utc_datetime = str(obs2.data[station_name]['times'][-1])
            utc_format = "%Y-%m-%d %H:%M:%S"
            local_tz = pytz.timezone('Europe/Helsinki')

            utc_dt = dt.datetime.strptime(utc_datetime, utc_format)
            local_dt = str(utc_dt.replace(
                tzinfo=pytz.utc).astimezone(local_tz))[:-6]
            # print("UTC", utc_datetime, "Local", local_dt)
        except KeyError:
            print("Following station not found. No data retrieved.")
            utc_datetime = None
            local_dt = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            get_error = 1

        if utc_datetime is not None:
            temperature = obs2.data[station_name]['Air temperature']['values'][-1]
            # print("Temperature:", temperature)

            wind = obs2.data[station_name]['Wind speed']['values'][-1]
            wind_direction = obs2.data[station_name]['Wind direction']['values'][-1]
            # print("Wind:", wind, "m/s direction:", wind_direction)
        else:
            temperature = None
            wind = None
            wind_direction = None

        return (temperature, wind, wind_direction, local_dt, get_error)

    def save_observation(self, station_id):
        """ Saves observation to the database.
            Args:
            station_id: id of the selected station
            connection: Connection-object for the database"""

        cursor = self._connection.cursor()
#        date = dt.datetime.now()
#        date_str = date.strftime('%d.%m.%Y %H:%M:%S')

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

    def find_observation(self, station_id):
        """Returns latest observations for a station.

            Returns:
                Observation objects.
            """

        cursor = self._connection.cursor()

        cursor.execute("select * from observations where station_id=? \
                       ORDER BY observation_id DESC LIMIT 1", (str(station_id),))

        row = cursor.fetchone()
        self._connection.commit()

        return get_observation_by_row(row)

    def delete_all(self):
        """Removes all observations from observations table.
        """

        cursor = self._connection.cursor()

        cursor.execute("delete from observations")

        self._connection.commit()


observation_repository = ObservationRepository(get_database_connection())

print("OBS REPO\n")
