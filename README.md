# My Weather Window application
With this application the user can view latest measurements from selected weather stations. Measurement data is retrieved from the open data provided by The Finnish Meteorological Institute.

This application is made as a course work in the Software engineering course (Aineopintojen harjoitustyö: Ohjelmistotekniikka) as part of Computer Science studies in the University of Helsinki.

## Documentation
- [User manual] TBD
- [Specifications](dokumentaatio/specifications.md)
- [Architecture] TBD
- [Testing document] TBD
- [Time tracking](dokumentaatio/timetracking.md)
- [Changelog](dokumentaatio/changelog.md)

## Installation
1. Install dependencies with shell command:

```bash
poetry install
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

### Generate the test coverage report 


```bash
poetry run invoke coverage-report
```

Report is generated to folder htmlcov_ 



## Tehtävät
### Viikko 1
[gitlog.txt](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/laskarit/viikko1/gitlog.txt)

[komentorivi.txt](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/laskarit/viikko1/komentorivi.txt)

### Viikko 2
[Screenshot.png](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/laskarit/viikko2/2024-03-20_viikko2_screenshot.png)

### Viikko 3
[arkkitehtuuri.md](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/laskarit/viikko3/arkkitehtuuri.md)

[sekvenssikaavio.md](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/laskarit/viikko3/sekvenssikaavio.md)

[changelog.md](https://github.com/mcpaulafi/ot-harjoitustyo/blob/main/dokumentaatio/changelog.md)
