# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Version [1.0.2] - 2024-01-02

### Changed

- Zurg: download release version parsing


## Version [1.0.1] - 2023-12-21

### Changed

- plex_debrid: increased read timeout to 5 seconds for GitHub repository checks 


## Version [1.0.0] - 2023-12-21

### Changed

- Automatic Updates: Breaking Change: AUTO_UPDATE env var renamed to PD_UPDATE
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

- Zurg: container pulls latest or user-defined version of ZURG from github upon startup


## Version [0.0.5] - 2023-12-06

### Fixed

- Duplicate Cleanup: process not called correctly


## Version [0.0.4] - 2023-12-06

### Changed

- Dockerfile: pull latest config.yml from zurg repo for base file


## Version [0.0.3] - 2023-12-05

### Changed

- Zurg: fix config.yml override


## Version [0.0.2] - 2023-12-05

### Changed

- base: update envs
- main.py: order of execution
- healthcheck.py: order of execution


## Version [0.0.1] - 2023-12-05

### Added

- Initial Push 