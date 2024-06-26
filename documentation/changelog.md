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

- User can select one station from station list view
- Application architecture file created and documentation started
- In UI, changed station_view.py to stationlist_view.py and created new station_view.py
- In UI, station_view.py shows selected station (there will be options for selecting measurement data)
- Selected station is saved on the database and all previous data is removed from there
- Name of the selected station is retrieved from database and returned as object
- Observations class created and retrieving data from FMI

# Week 5 
- User can select up to 5 stations from station list view
- Fixed grid settings
- All previous functions updated to support multiple selections
- Plans for the layout of settings and its operation not ready
- Weather data of the selected stations is looped on the Weather view
- Observation service test added

# Week 6
- Removed the plan to give user choice to select which observations are included, not enough time in this course to make it work
- Fixed station names on CSV show they match the search
- Added error handling if station is not found from FMI
- Stationlist view: handling of the first 0 row, layout fixing
- Station view: User can save nicknames to selected stations, additions to service, repository, db, weather_view
- Weather view: Missing data handling, button back to Settings
- Observations repository: fixed get to return one object
- Added services/observations_scheduler.py which checks for new observation data in every 10-20 minutes
- Made again entire station_service_test and observation_service_test
- Asked ChatGPT to explain user_repository in the referenceapp, and to help with obs_scheduler_test debugging and how to use MagicMock
- Added new tests to classes Station, ObservationService, ObservationRepository
- User manual added to documentation, updated also architecture, specs

# Week 7
- Testing documentation created
- Changed folder name dokumentaatio -> documentation
- From settings to Weather view, if latest observations are in the database, do not get new
- Check if observation datetime was old, made a function to observation repository, updated and modified dependent functionalities
- Code cleanup and splitting functions to shorter ones
- Made new tests and implemented MagicMock to unittests, learned and debugged with ChatGPT
- Added better graphics on layout and gave up on alternative weather view layout
- Code cleanup documentation to all python files
- Fixed bugs on selecting limit and last station running twice on the loop
- Error handling to received data
- Updated documentation