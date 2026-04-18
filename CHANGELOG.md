# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-19

### Added
- Refactored application into a modular package under `blinker/`.
- Added configurable CLI options for runtime behavior and camera settings.
- Added CSV event/session logging abstraction with summary metrics.
- Added unit tests for EAR math and blink detection state transitions.
- Added packaging metadata in `pyproject.toml`.
- Added repository badges and release tagging workflow.

### Changed
- Replaced monolithic `blink_counter.py` implementation with a thin entry-point wrapper to `blinker.cli`.
- Improved project documentation with setup, run, tuning, and troubleshooting guidance.

[1.0.0]: https://github.com/Rohit11-OG/Lid-Logic/releases/tag/v1.0.0
