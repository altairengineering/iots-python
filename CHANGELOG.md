# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0](https://github.com/altairengineering/iots-python/tree/v0.5.0) (2025-02-07)

## Changed

- Update the expected status code for Property update responses following recent
  changes in the API.

## [0.4.0](https://github.com/altairengineering/iots-python/tree/v0.4.0) (2024-09-05)

### Added

- Support for partial update of Things (`patch()` method).
- Support for sending emails using the Communications API.

### Changed

- Support sending lists with `make_request()`.
- Improve Content-Type validation.

## [0.3.0](https://github.com/altairengineering/iots-python/tree/v0.3.0) (2024-08-27)

### Added

- `verify` parameter to the `API` class to disable TSL certificate verification.

## [0.2.0](https://github.com/altairengineering/iots-python/tree/v0.2.0) (2024-04-09)

### Added

- Support for Python 3.8+.

### Fixed

- Wrong encoding when updating the value of a single Property for certain data
  types ([9e94271e](https://github.com/altairengineering/iots-python/commit/9e94271e)).
- Replace references to SmartWorks with IoT Studio.

## [0.1.1](https://github.com/altairengineering/iots-python/tree/v0.1.1) (2024-03-27)

### Changed

- Fix and update badges.

## [0.1.0](https://github.com/altairengineering/iots-python/tree/v0.1.0) (2024-03-27)

### Added

- 🚀 Initial release. It supports the following AnythingDB APIs:
  - Categories API
  - Things API
  - Properties API
  - Actions API
  - Events API
