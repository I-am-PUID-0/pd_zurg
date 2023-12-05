# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.1] - 2023-08-10

### Fixed

- healthcheck for rclone_RD mounts when plex_debrid standalone deployment is used 

## [1.4.0] - 2023-08-08

### Added

- alldebrid support
- independent simultaneous rclone_RD mounts 
- plex_debrid settings.json to automatically include alldebrid and realdebrid as debrid services

### Changed

- healthcheck process to monitor both alldebrid and realdebrid mounts 
- duplicate cleanup process to use alldebrid and realdebrid mounts

### Removed

- duplicate format_time function


## [1.3.1] - 2023-07-27

### Changed

- revert to single logger


## [1.3.0] - 2023-07-26

### Added

- duplicate cleanup

### Changed

- log rotation process
- healthcheck process - added delay for startup


## [1.2.7] - 2023-06-08

### Fixed

- check_log_rotation for log file name


## [1.2.6] - 2023-06-08

### Fixed

- check_log_rotation


## [1.2.5] - 2023-06-07

### Fixed

- log file name


## [1.2.4] - 2023-06-07

### Fixed

- logger import timedelta

## [1.2.3] - 2023-06-07

### Fixed

- logger startup process


## [1.2.2] - 2023-06-07

### Changed

- log rotation process


## [1.2.1] - 2023-06-07

### Fixed

- logger datetime

### Changed

- restrucure directory paths to be releative to the project root


## [1.2.0] - 2023-06-06

### Added

- support for .env file use

### Changed

- logger process


## [1.1.3] - 2023-06-06

### Fixed

- logger for ASCII Art


## [1.1.2] - 2023-06-06

### Fixed

- logger for ASCII Art & rclone setup


## [1.1.1] - 2023-06-06

### Fixed
- logger for ASCII Art & healthcheck
- typos


## [1.1.0] - 2023-06-06

### Added

- logger to file and console for pdrcrd


## [1.0.0] - 2023-06-06

### Added

- Changelog
- ASCII Art and Version Number