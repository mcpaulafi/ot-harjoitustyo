# Changelog
## Week 3

- User can view list of available stations
- index.py starts Tkinter window
- In UI, ui.py creates user interphase and stationlist_view.py requests and shows station list
- In UI, weather_view.py (will show selected station)
- Database initialization creates SQLite3 database and adds stations to it from the file
- Build runs initialize_database.py
- In Entities added Station class, which has all parameters for a weather station
- In Repositories added StationRepository class, which fetches from database and returns all Stations
- In Services added StationService class, which includes app logic related to Stations
- Test that StationService returns all 210 stations and a station name mathes its original_id

## Week 4

- User can select one station from station view
- Application architecture file created and documentation started
- In UI, changed station_view.py to stationlist_view.py and created new station_view.py
- In UI, station_view.py shows selected station (there will be options for selecting measurement data)
- Selected station is saved on the database and all previous data is removed from there
- Name of the selected station is retrieved from database and returned as object
- Observations class created and retrieving data from FMI
