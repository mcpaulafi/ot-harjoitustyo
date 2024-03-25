from database_connection import get_database_connection


def drop_tables(connection):
    """Poistaa tietokantataulut.

    Args:
        connection: Tietokantayhteyden Connection-olio
    """

    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists stations;
    """)

    connection.commit()


def create_tables(connection):
    """Luo tietokantataulut.

    Args:
        connection: Tietokantayhteyden Connection-olio
    """

    cursor = connection.cursor()

    cursor.execute("""
            create table stations (
            station_id integer NOT NULL,
            fmisid text,
            name text,
            nickname text,
            lat text,
            lon text,
            selected integer,
            PRIMARY KEY (station_id)
        );
    """)

    connection.commit()


def initialize_database():
    """Alustaa tietokantataulut."""

    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
