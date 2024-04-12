# Architecture
## Construction

Application has 3 level hierarchy, as follows

```mermaid
flowchart LR
    ui -.-> services
    services -.-> entities
    services -.-> repositories
    repositories -.-> entities
```

- **Ui**: user interphase
- **Services**: app logic
- **Repositories**: data storage
- **Entities**: class objects


## User interphase

User interphase contains 2 views:
- Settings
- Weather

Both are implemented as classes. Only one view is visible at the time to the user. Views are managed by UI class. User interphase is meant to be independent from the application logic and it utilizes methods from Service classes.

## Application logic

Data model of the application is constructed by classes Station and Observation which model weather stations and their observation data. 

[INSERT IMAGE]

Functions are in the Service classes StationService and ObservationService. 

**StationService** class provides following methods
- get_stations()

StationService has access to station data through StationRepository which is responsible of saving and retrieving data from the database.

Class and packing diagram for StationService and its dependencies to other application modules

[INSERT IMAGE HERE]

**ObservationService** class TBD.


## Data storage

Repository classes StationRepository and ObservationRepository are responsible for saving data to the database.

### Files

At the start the list of weather stations is uploaded to the database from a CSV file because they are not available from the open data of FMI.

Format in the file is following
```
"Ähtäri Inha",101520,62.55,24.14
"Alajärvi Möksy",101533,63.09,24.26
```

First on the row is the name of the station, then its id at FMI followed by latitude and longitude coordinates. Separation of the fields is made by comma character (,).

Stations are saved on SQLite database table called stations which is initialized on the file named initialize_database.py.

### Database

SQLite database tables are following 

```mermaid
 classDiagram
    Stations "*" --> "1..5" Selected_stations
    Selected_stations "1" -- "*" Observations
    class Settings {
        layout
    }
    class Stations {
        station_id
        name
        nickname
        original_id
        lat
        lon
        source
    }
    class Selected_stations {
        station_id
        temperature
        wind
    }
    class Observations {
        observation_id
        station_id
        datetime
        temperature
        wind
        wind_direction
    }

```

## Main functions

Next the basic application logic is described on the sequence diagrams.

### Selecting stations
On Settings view the user first selects a weather station from the listbox and then clicks the _Select_ button. 

```mermaid
sequenceDiagram
    User->> UI: click "Select" button
    UI->>UI: Show_selection

```

On Settings after selecting a station user can rename the station and select observations for it. Then user clicks the _Save and view_ button. 

```mermaid
sequenceDiagram
    User->> UI: click "View" button
    UI->>StationService: save_selected()
    StationService->>StationRepository: save_selected()
    StationRepository-->>StationService: station_id
    StationService-->>UI: station_id
    UI->>UI: View_weather()

```


## Renaming station

After the selection user can rename the station (give a nickname such as "Summer cabin"). TBD

## Selecting observations

After the selection user can also select which observation data (temperature, wind) is retrieved from the station. TBD

## Selecting layout

User can also select the layout for the weather view from some options. TBD

### Weather view

Weather view shows the latest observation data from the selected station. TBD


User can return to settings.


## Data update from FMI
TBD!