# Specifications for My Weather Station Window

## Meaning of the application

With this application the user can view latest measurements from selected weather stations. Measurement data is retrieved from the open data provided by The Finnish Meteorological Institute.

## Users

Application has only one user role.

## User interface

- User can choose weather stations which data is retrieved and shown (TEHTY)
- Data of selected stations in a loop (TEHTY) OR side by side
- User can choose which layout to use

## Main functionalities

### Select stations view (TEHTY)

User selects 1-5 weather stations from a list of available stations. 

### Station settings view

User can rename selected stations. (TEHTY)

User can select layout for weather view. 

Settings are saved to the database. Settings can be changed anytime. (TEHTY)

### Weather view (TEHTY)

Selected information is displayed on the view.

### Data updates (TEHTY)

Latest measurement data is retrieved every 10-20 minutes and saved on the database.

### Database (TEHTY)

SQLite database contains 4 tables 
- Stations
- Settings
- Selected_stations
- Observations

### Station list (TEHTY)
Stations are uploaded to the database from a csv-file. 

## Known bugs
- Not enough error handling yet
- Listbox mixes some station ID:s
- Not all stations deliver data for temperature and/or wind

## Development ideas / todos
- Create child object SelectedStations whose parent is Station
- User defines what measurement data (temperature, wind) is retrieved from the selected stations. (Not enough time to finnish in the course schedule)
- Split database table Observations per measurement
- More measurement data eg. rain
- Adding a Ruuvi tag from a private database as one option for a weather station
