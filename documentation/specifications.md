# Specifications for My Weather Station Window

## Meaning of the application

With this application the user can view latest measurements from selected weather stations. Measurement data is retrieved from the open data provided by The Finnish Meteorological Institute.

## Users

Application has only one user role.

## User interface

- User can choose weather stations which data is retrieved and shown.
- User can rename station
- Data of selected stations is shown in a loop

## Main functionalities

### Select stations view

User selects 1-5 weather stations from a list of available stations. 

### Station settings view

User can rename selected stations.

Settings are saved to the database. Settings can be changed anytime.

### Weather view 

Observations from selected station is displayed on the view. 
View switches to next station in 20 seconds.

### Data updates

Latest measurement data is retrieved every 10-60 minutes and saved on the database. If new data is not available for the station, requests slow down.

### Database

SQLite database contains 4 tables 
- Stations
- Settings
- Selected_stations
- Observations

### Station list
Stations are uploaded to the database from a csv-file. 

## Known bugs
- Not all stations deliver data for temperature and/or wind, application does not know which
- Fmiopendata sometimes crashes after application has been running more than 10 minutes

## Development ideas / todos
- Alternative WeatherView which shows all selected stations at once
- Create child object SelectedStations whose parent is Station
- User defines what measurement data (temperature, wind) is retrieved from the selected stations.
- Split database table Observations per different kind of measurements
- More measurement data options eg. rain
- Adding a Ruuvi tag from a private database as one option for a weather station
