# Changelog
## Week 3

- User can view list of available stations
- index.py starts Tkinter window
- In UI, ui.py creates user interphase and station_view.py requests and shows station list
- Database initialization creates SQLite3 database and adds stations to it from the file
- Build runs initialize_database.py
- In Entities added Station class, which has all parameters for a weather station
- In Repositories added StationRepository class, which fetches from database and returns all Stations
- In Services added StationService class, which includes app logic related to Stations
- NOT READY: Test that StationService returns all stations
