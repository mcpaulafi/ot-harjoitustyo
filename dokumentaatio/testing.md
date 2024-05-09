# Testing document

Application has been tested with `unittest` including automated unit and integration tests. System level tests have been made manually.

## Unit and integration testing 

### Application logic

The application logic in the following classes is tested as follows.

- `StationService` class tests are on [TestStationService`](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/src/tests/services/station_service_test.py)

`StationService` object is installed so that it is injected with `FakeStationRepository` object which saves data in to memory instead of database.

- `ObservationService` class tests are on [TestObservationService](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/src/tests/services/observation_service_test.py)

`ObservationService` object is installed so that it is injected with fake repository objects which save data in to memory and not in the database. For this use there are classes `FakeStationRepository`, `FakeStationService` and `FakeObservationRepository`.

- `Scheduler` class tests are on [TestObservationScheduler](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/src/tests/services/observation_scheduler_test.py)

`Scheduler` object is installed so that it is injected with fake repository objects which save data in to memory and not in the database. For this use there are classes
`FakeObservationRepository` and `FakeObservationService`.


### Repository classes

- Repository class `ObservationRepository` is tested with [TestObservationRepository](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/src/tests/repositories/observation_repository_test.py).

Tests use mock and MagicMock libraries from unittest to simulate database.

### Entity classes

- Methods in the entity class `Station` are tested with [TestStation](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/src/tests/entities/station_test.py)

### Test coverage

Application test branch coverage is ?% excluding the layer of user interface.

[INSERT IMAGE]

[INSERT LIST OF WHAT IS NOT TESTED]

## System tests

System test is done manually.

### Installing and configuration

Application has been downloaded and tested by following [the user manual](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/dokumentaatio/usermanual.md) in two different Linux environments. Tests did not check different configurations on  _.env_ file.

### Functionalities

All [specifications](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/dokumentaatio/specifications.md) and functionalities listed on the user manual have been checked. Also attempts have been made to fill input fields with false values such as empty ones.

## Remaining quality issues

There are no error messages in following cases:

- No read/write access to configuration files
- SQLite database has not been installed, `python -m poetry run invoke build` command is not run