# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains scripts to build and install dependencies required for the ASiMoV-CCS project on various systems including Cray A2, GNU/Linux, and macOS.

## Installation Methods

The repository provides two methods for installing dependencies:

1. **Legacy Bash Scripts** - The original installation method
2. **Python-based Installation** - The newer, recommended method with improved maintainability and error handling

## Python-based Architecture (Recommended)

### Dependency Management with Poetry

The Python-based installation uses [Poetry](https://python-poetry.org/) for dependency management. Poetry handles:

- Package dependencies (defined in `pyproject.toml`)
- Virtual environment creation
- Script entry points

### Directory Structure

- `config/` - YAML configuration files for different environments
- `ccs_dep/` - Python package containing:
  - `installers/` - Python modules for installing dependencies
  - `utils/` - Utility modules for commands, environment setup, etc.
  - `install.py` - Main installation script (Poetry entry point: `ccs-install`)
  - `setup.py` - Environment configuration script (Poetry entry point: `ccs-setup`)
- `pyproject.toml` - Poetry configuration file
- `tests/` - Test modules for installers and utilities

### Configuration System

The Python system uses YAML files for configuration:

- `config/default_config.yml` - Default configuration for all environments
- `config/gnu_macos.yml` - macOS-specific configuration
- `config/gnu_ubuntu.yml` - Ubuntu-specific configuration
- `config/cray_A2.yml` - Cray-specific configuration

### Build Directory

The Python implementation determines the build directory in a cross-platform way using `tempfile.gettempdir()`. This ensures that the build directory is placed appropriately:

- On Linux: typically `/tmp`
- On macOS: typically `/var/folders/...`
- On Windows: typically `C:\Users\<username>\AppData\Local\Temp`
- On BSD: typically `/tmp`

### Required Dependencies

The following Python packages are required:

- `pyyaml` - For YAML configuration file parsing
- `distro` - For system distribution detection
- `poetry-core` - For Poetry integration
- `cmake` - For building some dependencies
- `gitpython` - For Git repository operations

### Commands

When using Poetry:

```bash
# Install with Poetry
poetry install

# Install all dependencies for the detected environment
poetry run ccs-install

# Specify environment explicitly
poetry run ccs-install --env gnu_macos

# Install specific dependencies
poetry run ccs-install --dependencies hdf5,petsc

# Configure environment for building CCS
eval $(poetry run ccs-setup --env gnu_macos)

# Show version information
poetry run ccs-install --version
poetry run ccs-setup --version

# Debug mode for troubleshooting
poetry run ccs-install --debug
```

Without Poetry:

```bash
# Directly run the scripts
./install.py --env gnu_macos
eval $(./setup.py --env gnu_macos)
```

## Legacy Bash Scripts

### Environment Setup

The environment is configured via setup scripts:
- `setup_base.sh` - Contains common environment variables and dependency versions
- Platform-specific setup scripts (e.g., `setup_gnu_ubuntu.sh`, `setup_cray_A2.sh`, `setup_gnu_macos.sh`) 

### Key Environment Variables

- `INSTALL_DIR` - Directory where dependencies will be installed (default: `$HOME/ccs-deps`)
- `BUILD_DIR` - Temporary directory for building dependencies (default: `/tmp/build-ccs-deps`)
- `ENV` - Specifies the target environment/platform (e.g., `gnu_ubuntu`, `cray_A2`, `gnu_macos`)
- `CMP` - Compiler type, extracted from ENV (e.g., `gnu`, `cray`)

### Installation Commands

```bash
# Install dependencies for a specific environment
ENV=gnu_ubuntu ./install_base.sh
# or
ENV=gnu_macos ./install_base.sh
```

## Available Dependencies

The repository installs the following dependencies:

- makedepf90 - Fortran dependency generator
- fyaml_c - YAML parser in C
- hdf5 - Hierarchical Data Format library
- adios2 - Adaptable I/O System for scientific data
- petsc - Portable, Extensible Toolkit for Scientific Computation
- parhip - Parallel High-quality Graph Partitioning
- parmetis - Parallel Graph Partitioning and Fill-reducing Matrix Ordering
- rcm_f90 - Reverse Cuthill-McKee algorithm in Fortran 90
- python_deps - Python dependencies (PyYAML, LIT, etc.)

## Dependency Versions

The default dependency versions (defined in both `setup_base.sh` and `config/default_config.yml`):

- ADIOS2: 2.10.1
- ParHIP: 3.14
- PETSc: 3.21.2
- HDF5: 1.14.4.3
- FYAML-C: 0.2.5
- RCM-f90: 1.0.0

## Building CCS After Dependencies

After installing dependencies:

### Python Setup with Poetry

```bash
# Configure environment using Poetry
eval $(poetry run ccs-setup --env gnu_macos)

# Then clone and build CCS
git clone git@github.com:asimovpp/asimov-ccs.git
cd asimov-ccs
make all
```

### Python Setup without Poetry

```bash
# Configure environment using Python setup
eval $(./setup.py --env gnu_macos)

# Then clone and build CCS
git clone git@github.com:asimovpp/asimov-ccs.git
cd asimov-ccs
make all
```

### Legacy Bash Setup

```bash
# Source the appropriate environment setup script
source setup_gnu_ubuntu.sh
# or 
source setup_gnu_macos.sh

# Then clone and build CCS
git clone git@github.com:asimovpp/asimov-ccs.git
cd asimov-ccs
make all
```

## Installation Workflow (Python Method with Poetry)

1. Install Poetry: `curl -sSL https://install.python-poetry.org | python3 -`
2. Install dependencies: `poetry install`
3. Run installer: `poetry run ccs-install [--env <environment>]`
4. Configure environment: `eval $(poetry run ccs-setup [--env <environment>])`
5. Clone and build the main CCS project

## Installation Workflow (Python Method without Poetry)

1. Install Python requirements: `pip install -r requirements.txt`
2. Run `./install.py [--env <environment>]` to install all dependencies
3. Configure environment with `eval $(./setup.py [--env <environment>])`
4. Clone and build the main CCS project

## Installation Workflow (Bash Method)

1. Configure environment variables in `setup_base.sh` or use defaults
2. Run `ENV=<environment> ./install_base.sh` to install all dependencies
3. Source the appropriate setup script for your platform
4. Clone and build the main CCS project

## Development

For developers working on extending the Python-based installation system:

1. Create a Poetry shell environment: `poetry shell`
2. Run the commands directly: `ccs-install --debug`
3. Run code formatting: `poetry run black .` 
4. Run linting: `poetry run pylint installers utils`

## Testing

The repository includes a test suite for the installer modules. These tests use ephemeral sandboxes to ensure complete isolation and cleanup.

### Running Tests

```bash
# Run all installer tests with Poetry
poetry run pytest tests/

# Run a specific installer test
poetry run pytest tests/test_hdf5_installer.py

# Run tests with the test runner script
poetry run python tests/run_installer_tests.py

# Run tests with more detailed output
poetry run pytest -xvs tests/
```

### Test Structure

- `tests/test_installers_base.py` - Base test class with common functionality
- `tests/test_hdf5_installer.py` - Tests for HDF5 installer
- `tests/test_parmetis_installer.py` - Tests for ParMETIS installer
- `tests/test_petsc_installer.py` - Tests for PETSc installer
- `tests/run_installer_tests.py` - Script to run all installer tests

The tests are designed to be completely ephemeral:
- Each test creates temporary build and install directories
- External dependencies (Git, command execution) are mocked
- All temporary resources are cleaned up after the tests run
- No actual building or installation occurs during testing

### Adding New Tests

To add tests for a new installer:

1. Create a new test file in the `tests/` directory
2. Extend the `BaseInstallerTest` class
3. Implement test methods for each phase of installation
4. Update `run_installer_tests.py` to include the new test file

## Error Handling

The Python implementation includes improved error handling:
- Type conversion for environment variables (ensuring all values are strings)
- Cross-platform temporary directory detection
- Clear error messages for configuration and dependency issues 
- Debug mode for troubleshooting with `--debug` flag
- Robust Git operations with GitPython for repository cloning
- Fallback mechanisms for download operations (wget, curl, Python urllib)
- Path handling with pathlib for cross-platform compatibility