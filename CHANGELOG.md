# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-05-21

### Added
- Added GitPython as a dependency
- Created test for GitPython functionality
- Added GitHub workflow for testing GitPython integration

### Changed
- Updated `clone_repository` function to use GitPython instead of shell commands
- Refactored all file path handling to use pathlib.Path instead of os.path
- Improved error handling in repository cloning operations
- Added automatic directory creation for file download and extraction operations

## [0.1.0] - 2025-05-20

### Added
- Initial release
- Poetry support for dependency management
- Python-based installation system
- Support for macOS, Ubuntu, and Cray A2 environments
- Cross-platform build directory handling