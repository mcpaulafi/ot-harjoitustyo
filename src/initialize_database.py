import os
from database_connection import get_database_connection
from pathlib import Path

"""File which includes list of available stations."""
# TODO: get file name from global settings

dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "..", "data", "fmi_stations.csv")

def ensure_file_exists():
    """Checking the file.
    
    Args: 
        file_path: file to be tested
    """
    Path(file_path).touch()


def drop_tables(connection):
    """Remove databases.

    Args:
        connection: Connection-object for the database
    """

    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists stations;
    """)

    connection.commit()


def create_tables(connection):
    """Create tables on the database.
        TODO: includes only stations 

    Args:
        connection: Connection-object for the database
    """

    cursor = connection.cursor()

    cursor.execute("""
            create table stations (
            station_id integer NOT NULL,
            original_id text,
            name text,
            nickname text,
            lat text,
            lon text,
            source text,
            PRIMARY KEY (station_id)
        );
    """)

    connection.commit()


def read_stations_from_file(file_path):
    """ Read stations from the file to a list. Return list.

    Args: 
        file_path: file to be read
    """
    stations = []

    ensure_file_exists()

    with open(file_path) as file:
        for row in file:
            #print("row", row)
            row = row.replace("\n", "")
            row = row.replace("\"", "")
            parts = row.split(",")

            name = parts[0]
            original_id = parts[1]
            lat = parts[2]
            lon = parts[3]
            if name != "Name" or name=="name":
                stations.append(
                    [name, original_id, lat, lon]
                )
    return stations


def upload_stations_to_database(station_list, connection):
        """ Upload stations from list to the database table stations.

        Args:
            parts: list of stations
            connection: Connection-object for the database
        """
        for station_data in station_list:
            name = station_data[0]
            nickname = ""
            original_id = station_data[1]
            lat = station_data[2]
            lon = station_data[3]
            source = "FMI"
            cursor = connection.cursor()

            cursor.execute(
                '''insert into stations (name, nickname, original_id, lon, lat, source) values (?, ?, ?, ?, ?, ?)''',
                (str(name), str(nickname), str(original_id), str(lon), str(lat), str(source))
            )

            connection.commit()

def initialize_database():
    """Initializes database tables and uploads stations from the file to the database."""

    connection = get_database_connection()

    read_stations=read_stations_from_file(file_path)

    drop_tables(connection)
    create_tables(connection)
    upload_stations_to_database(read_stations, connection)

    print("Database created.")


if __name__ == "__main__":
    pass
    initialize_database()
    #Print file content
    #print(read_stations_from_file(file_path))