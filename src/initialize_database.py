from pathlib import Path
from config import STATIONS_FILE_PATH
from database_connection import get_database_connection

# File which includes list of available stations from FMI.
file_path = STATIONS_FILE_PATH


def ensure_file_exists():
    """Checking the file.

    Args: 
        file_path: file to be tested
    """
    if Path(file_path).touch():
        return True
    return False


def drop_tables(connection):
    """Remove databases.

    Args:
        connection: Connection-object for the database
    """

    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists stations;
    """)
    cursor.execute("""
        drop table if exists selected_stations;
    """)
    cursor.execute("""
        drop table if exists settings;
    """)
    cursor.execute("""
        drop table if exists observations;
    """)
    connection.commit()
    return True


def create_tables(connection):
    """Create tables on the database.
    Args:
        connection: Connection-object for the database
    """

    cursor = connection.cursor()

    cursor.execute("""
        create table stations (
        station_id integer NOT NULL,
        original_id text,
        name text,
        lat text,
        lon text,
        source text,
        PRIMARY KEY (station_id)
    );
    """)
    cursor.execute("""
        create table selected_stations (
        station_id integer NOT NULL,
        nickname text,
        temperature integer DEFAULT 0 NOT NULL,
        wind text integer DEFAULT 0 NOT NULL,
        datetime text,
        PRIMARY KEY (station_id)
    );
    """)
    cursor.execute("""
        create table settings (
        layout integer DEFAULT 1 NOT NULL
    );
    """)
    cursor.execute("""
        create table observations (
        observation_id integer NOT NULL,
        station_id integer NOT NULL,
        datetime text,
        temperature text,
        wind text,
        wind_direction text,
        error_msg integer DEFAULT 0,
        PRIMARY KEY (observation_id)
    );
    """)

    connection.commit()
    return True


def read_stations_from_file(file_path2):
    """ Read stations from the file to a list. Return list.

    Args: 
        file_path: file to be read
    """
    stations = []

    ensure_file_exists()

    with open(file_path2, encoding="utf-8") as file:
        for row in file:
            # print("row", row)
            row = row.replace("\n", "")
            row = row.replace("\"", "")
            parts = row.split(",")

            name = parts[0]
            original_id = parts[1]
            lat = parts[2]
            lon = parts[3]
            if name != "Name" or name == "name":
                stations.append(
                    [name, original_id, lat, lon]
                )
    return stations


def upload_stations_to_database(station_list, connection):
    """ Upload stations from list to the database table stations.
    Args:
    parts: list of stations
    connection: Connection-object for the database"""
    for station_data in station_list:
        name = station_data[0]
        original_id = station_data[1]
        lat = station_data[2]
        lon = station_data[3]
        source = "FMI"
        cursor = connection.cursor()

        cursor.execute(
            '''insert into stations (name, original_id, lon, lat, source) 
            values (?, ?, ?, ?, ?)''',
            (str(name), str(original_id), str(lon), str(lat), str(source))
        )

        connection.commit()
    return True


def initialize_database():
    """Initializes database tables and uploads stations from the file to the database."""

    connection = get_database_connection()

    read_stations = read_stations_from_file(file_path)

    drop_tables(connection)
    create_tables(connection)
    upload_stations_to_database(read_stations, connection)

    print("Database created.")
    return True
