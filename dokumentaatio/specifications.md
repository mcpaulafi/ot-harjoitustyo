# Specifications for My Weather Station Window

## Meaning of the application

With this application the user can view latest measurements from selected weather stations. Measurement data is retrieved from the open data provided by The Finnish Meteorological Institute.

## Users

Application has only one user role.

## User interface

TBD:
- On a slider one weather station at a time /or stations side by side.
- User can choose which layout to use

## Main functionalities

### Settings

User selects 1-5 weather stations and their measurement data (temperature, wind). User can rename selected stations. User can select layout for weather view. Settings are saved to the database. Settings can be changed anytime.

### Weather view

Selected information is displayed on the view.

### Data updates 

Latest measurement data is retrieved every hour and saved on the database.

### Database

SQLite database contains 4 tables
- Stations
- Settings
- Selected_stations
- Observations

### Station list
Stations are uploaded to the database from a csv-file.

## Development ideas / todos
- Split database table Observations per measurement
- More measurement data eg. rain
- Adding a Ruuvi tag from a private database as one option for a weather station
