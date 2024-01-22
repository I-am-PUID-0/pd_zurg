# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Version [2.0.3] - 2024-01-22

### Fixed

- plex_debrid: Fixed Plex users for Jellyfin deployments


## Version [2.0.2] - 2024-01-22

### Fixed

- PLEX_REFRESH: Fixed Plex library refresh w/ Zurg when using docker secrets

## Version [2.0.1] - 2024-01-16

### Fixed

- logging: Fixed logging for subprocesses


## Version [2.0.0] - 2024-01-04

### Breaking Change

- PD_ENABLED: Added PD_ENABLED env var to enable/disable plex_debrid service
- PLEX_USER: PLEX_USER env var no longer enables plex_debrid service

### Added

- JF_API_KEY: JF_API_KEY env var added to enable Jellyfin integration
- JF_ADDRESS: JF_ADDRESS env var added to enable Jellyfin integration
- SEERR_API_KEY: SEERR_API_KEY env var added to enable Overseerr/Jellyseerr integration
- SEERR_ADDRESS: SEERR_ADDRESS env var added to enable Overseerr/Jellyseerr integration
- PLEX_REFRESH: PLEX_REFRESH env var added to enable Plex library refresh w/ Zurg
- PLEX_MOUNT_DIR: PLEX_MOUNT_DIR env var added to enable Plex library refresh w/ Zurg

### Changed

- plex_debrid setup: plex_debrid setup process now allows for selection of Plex or Jellyfin

### Removed

- ZURG_LOG_LEVEL: Removed the need for ZURG_LOG_LEVEL env var - now set by PDZURG_LOG_LEVEL
- RCLONE_LOG_LEVEL: Removed the need for RCLONE_LOG_LEVEL env var - now set by PDZURG_LOG_LEVEL


## Version [1.1.0] - 2024-01-04

### Added

- Docker Secrets: Added support for the use of docker secrets


## Version [1.0.3] - 2024-01-03

### Changed

- Zurg: Increased read timeout to 10 seconds for GitHub repository checks
- Zurg: Setup process now checks for existing config.yml in debrid service directory
- Zurg: Setup process now checks for existing zurg app in debrid service directory
- Logging: Cleaned up logging and added additional logging details

## Version [1.0.2] - 2024-01-02

### Changed

- Zurg: Download release version parsing


## Version [1.0.1] - 2023-12-21

### Changed

- plex_debrid: increased read timeout to 5 seconds for GitHub repository checks 


## Version [1.0.0] - 2023-12-21

### Breaking Change

- Automatic Updates: AUTO_UPDATE env var renamed to PD_UPDATE

### Changed

- Automatic Updates: Refactored update process to allow for scaling of update process
- Healthcheck: Refactored healthcheck process to allow for scaling of healthcheck process
- Healthcheck: rclone mount check now uses rclone process instead of rclone mount location
- Rclone: Subprocess logs are now captured and logged to the pd_zurg logs

### Added

- ZURG_UPDATE: ZURG_UPDATE env var added to enable automatic update process for ZURG
- Zurg: Added automatic update process for Zurg
- Healthcheck: Added healthcheck for Zurg process


## Version [0.2.0] - 2023-12-13

### Added

- ZURG_LOG_LEVEL: The log level to use for Zurg as defined with the ZURG_LOG_LEVEL env var


## Version [0.1.0] - 2023-12-12

### Added

- ZURG_VERSION: The version of ZURG to use as defined with the ZURG_VERSION env var 

### Changed

- Zurg: Container pulls latest or user-defined version of ZURG from github upon startup


## Version [0.0.5] - 2023-12-06

### Fixed

- Duplicate Cleanup: Process not called correctly


## Version [0.0.4] - 2023-12-06

### Changed

- Dockerfile: Pull latest config.yml from zurg repo for base file


## Version [0.0.3] - 2023-12-05

### Fixed

- Zurg: config.yml override


## Version [0.0.2] - 2023-12-05

### Changed

- base: Update envs
- main.py: Order of execution
- healthcheck.py: Order of execution


## Version [0.0.1] - 2023-12-05

### Added

- Initial Push 