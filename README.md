# My Weather Window application
With this application the user can view latest measurements from selected weather stations. Measurement data is retrieved from the open data provided by The Finnish Meteorological Institute (FMI).

Python interphase for FMI open data is from [fmiopendata](https://github.com/pnuu/fmiopendata)

This application is made as a course work in the Software engineering course (Aineopintojen harjoitustyö: Ohjelmistotekniikka) as part of Computer Science studies in the University of Helsinki.

## Documentation
- [User manual](dokumentaatio/usermanual.md)
- [Specifications](dokumentaatio/specifications.md)
- [Architecture](dokumentaatio/architecture.md)
- [Testing document] TBD
- [Time tracking](dokumentaatio/timetracking.md)
- [Changelog](dokumentaatio/changelog.md)

## Releases

- [Viikko5](https://github.com/mcpaulafi/ot-harjoitustyo/releases/tag/viikko5) 22.4.2024
- [Viikko6](https://github.com/mcpaulafi/ot-harjoitustyo/releases/tag/viikko6) 30.5.2024

## Installation

1. Start Poetry. Install dependencies with shell command:

```bash
poetry install --no-root
```

2. Run required initialization operations with shell command:

```bash
poetry run invoke build
```

3. Start application with shell command:

```bash
poetry run invoke start
```
## Shell commands

### Run application

```bash
poetry run invoke start
```

### Run tests

```bash
poetry run invoke test
```

### Run Pylint

```bash
poetry run invoke lint
```

### Generate the test coverage report 


```bash
poetry run invoke coverage-report
```

Report is generated to folder htmlcov_ 
