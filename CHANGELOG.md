# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0]

### Added
- This `CHANGELOG.md` file.
- `mypy` and `isort` as development dependencies.
- `wallhaven/__version__.py` to keep track of the project's current version.
- `wallhaven.exceptions.WallhavenException`.

### Changed
- Rewrite everything from scratch.
- Rename `wallhaven/main.py` to `wallhaven/api.py`.
- Rename `wallhaven/params.py` to `wallhaven/config.py`
- Increase line-length to 90 characters.
- `utils.py` is now a single file shared project-wide.

### Removed
- Delete every line of code. 
- `wallhaven.params` and `wallhaven.Wallhaven` classes.
- Author's and `wallhaven` version from `wallhaven/__init__.py`. 
- All exceptions from `wallhaven/exceptions.py`.
