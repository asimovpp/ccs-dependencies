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
- `installers/` - Python modules for installing dependencies
- `utils/` - Utility modules for commands, environment setup, etc.
- `install.py` - Main installation script (Poetry entry point: `ccs-install`)
- `setup.py` - Environment configuration script (Poetry entry point: `ccs-setup`)
- `pyproject.toml` - Poetry configuration file

### Configuration System

The Python system uses YAML files for configuration:

- `config/default_config.yml` - Default configuration for all environments
- `config/gnu_macos.yml` - macOS-specific configuration
- `config/gnu_ubuntu.yml` - Ubuntu-specific configuration
- `config/cray_A2.yml` - Cray-specific configuration

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