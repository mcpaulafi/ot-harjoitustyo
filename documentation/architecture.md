# Architecture
## Structure

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
- **Repositories**: data storage, retrieving data from API
- **Entities**: class objects


## User interphase

User interphase contains 3 views:
- Select stations
- Settings
- Weather

Views are implemented as classes. Only one view is visible at the time to the user. Views are managed by UI class. User interphase is meant to be independent from the application logic and it utilizes methods from Service classes.

## Application logic

Data model of the application is constructed by classes Station and Observation which model weather stations and their observation data. 
```mermaid
 classDiagram
    Stations <--> Observations
    class Stations {
        station_id
        original_id
        name
        nickname
        lat
        lon
        source
        error_msg
    }
    class Observations {
        station_id
        temperature
        wind
        wind_direction
        datetime
        error_msg
    }
```

Classes have following funcions.

**Station** class provides following methods
- set_nickname(nickname)
- get_nickname()
- set_error_msg(error_msg)
- get_error_msg()

**StationService** class provides following methods
- get_stations()
- get_station()
- count_all()
- delete_all()
- count_selected()
- save_selected(station_id)
- save_selected_nickname(station_id, nickname)
- get_selected()
- get_nickname(self, station_id)
- get_error(self, station_id)
- delete_selected()

StationService has access to station data through StationRepository which is responsible of saving and retrieving data from the database. 

Class and packing diagram for StationService and its dependencies to other application modules

[INSERT IMAGE HERE]

**Observation** class has no methods.

**ObservationService** class procides following methods
- get_observation(station_id)
- update_observation(station_id)
- delete_observations_from_database()

ObservationService has access to the database through ObservationRepository.

**ObservationScheduler** gets new observation data every 10-20 minutes. It is started by the WeatherWindow class. This class provides following method
- scheduled_observation_update()



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
    class Stations {
        station_id
        name
        original_id
        lat
        lon
        source
    }
    class Selected_stations {
        station_id
        nickname
        temperature
        wind
        datetime
    }
    class Observations {
        observation_id
        station_id
        datetime
        temperature
        wind
        wind_direction
        error_msg
    }

```

## Main functions

Next the basic application logic is described on the sequence diagrams.

### Selecting stations
On Stationslist_view the user first selects a weather station from the listbox and then clicks the _Select_ button. Selection is saved on the database and view is switched to Station_view, which shows options for the selected station. 

```mermaid
sequenceDiagram
    actor User
    participant UI
    participant StationService
    participant StationRepository

    rect rgb(156, 156, 156)
    note right of UI: init
    UI->>StationService :get_stations()
    StationService-->>UI: list of Stations objects
    end

    loop 1-5 selections
        User->> UI: click "Add to >" button
        UI->>StationService: save_selected(station_id)
        StationService->>StationRepository: save_selected_stations_to_database(station_id)

        UI->>UI: _get_selected_list()
        UI->>StationService: get_selected()
        StationService-->>UI: list: station.name
        UI->>UI: _check_selected_count()
    end 

    User->> UI: click "Continue >" button
    UI->>UI: switch view (station_view)

```

### Settings for selected station

After the selection user can rename the station (give a nickname such as "Summer cabin"). 


```mermaid
sequenceDiagram
    actor User
    participant UI
    participant StationService
    participant StationRepository
    participant ObservationService
    participant ObservationRepository

    UI->>UI: _initialize_stations
    UI->>StationService : get_selected()
    StationService-->>UI: list: Stations

    loop User can input 0-5 nicknames
        User->> UI: input entry: nickname
    end

    User->> UI: click "Save and view" button

    loop all selected stations
    UI->>StationService: save_selected_nickname(station_id, nickname)
    StationService->>StationRepository: save_nickname_to_database(station_id, nickname)
    end

    StationService->>ObservationService: observation_service.update_observation(station_id)
    ObservationService->>ObservationRepository: save_observation(station_id)

    UI->>UI: switch view (weather_view)


```


### Weather view

On station_view when user clicks the _Save and view_ button application swithes to weather_view and gets measurement data for the selected station(s). 

```mermaid
sequenceDiagram
    participant UI
    participant StationService
    participant StationRepository
    participant ObservationService
    participant ObservationRepository

    rect rgb(156, 156, 156)
    note right of UI: init
    UI->>StationService: get_selected()
    StationService->>StationRepository: find_selected()
    StationRepository-->>StationService: station_id, temperature, wind
    StationService-->>UI: station_id, temperature, wind
    end

    UI->>UI: _update_view(), station_loop
    UI->>StationService: get_nickname(station_id)
    StationService->>StationRepository: find_nickname(station_id)
    StationRepository-->>StationService: Station
    StationService-->>UI: Station
    UI->>StationService: get_name(station_id)
    StationService->>StationRepository: find_name(station_id)
    StationRepository-->>StationService: Station
    StationService-->>UI: Station
    UI->>UI: Name label
    UI->>ObservationService: get_observation(station_id)
    ObservationService->>ObservationRepository: find_observation(station_id)
    ObservationRepository-->>ObservationService: temperature, wind, wind_direction, datetime, error_msg
    ObservationService-->>UI: temperature, wind, wind_direction, datetime, error_msg
    UI->>UI: Data Labels
    UI->>UI: After 10sec, update_view 
```


## Data update from FMI
If Weather View gets observation time that is older than 10 min, new data is requested from the Scheduler.

```mermaid
sequenceDiagram
    participant Scheduler
    participant ObservationService
    participant ObservationRepository
    participant FMIOpenData

    rect rgb(102, 102, 102)
    note right of Scheduler: init
    Scheduler->>ObservationService: init Selected stations
    ObservationService->>ObservationRepository: get selected()
    ObservationRepository-->>ObservationService: Stations
    ObservationService-->>Scheduler: Stations
    end

    UI->>Scheduler: scheduled_observation_update()
    Scheduler->>ObservationService: get_observation(station_id)
    ObservationService-->>Scheduler: Observation object
    Scheduler->>ObservationService: update_observation(station_id)
    ObservationService->>ObservationRepository: save_observation(station_id)
    ObservationRepository->>StationService: get_station(station_id)
    StationService-->>ObservationRepository: True
    ObservationRepository->>ObservationRepository: get_data_from_fmi(station_id)
    ObservationRepository->>FMIOpenData: download_stored_query()
    FMIOpenData-->>ObservationRepository: data
    ObservationRepository-->>ObservationService: True
    ObservationService-->>Scheduler:True

```
