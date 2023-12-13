# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## Version [0.2.0] - 2023-12-13

### Added

- ZURG_LOG_LEVEL: The log level to use for Zurg as defined with the ZURG_LOG_LEVEL env var


## Version [0.1.0] - 2023-12-12

### Added

- ZURG_VERSION: The version of ZURG to use as defined with the ZURG_VERSION env var 

### Changed

- zurg: container pulls latest or user-defined version of ZURG from github upon startup


## Version [0.0.5] - 2023-12-06

### Fixed

- Duplicate Cleanup: process not called correctly


## Version [0.0.4] - 2023-12-06

### Changed

- Dockerfile: pull latest config.yml from zurg repo for base file


## Version [0.0.3] - 2023-12-05

### Changed

- zurg: fix config.yml override


## Version [0.0.2] - 2023-12-05

### Changed

- base: update envs
- main.py: order of execution
- healthcheck.py: order of execution


## Version [0.0.1] - 2023-12-05

### Added

- Initial Push 