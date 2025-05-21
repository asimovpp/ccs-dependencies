# CCS Dependencies

Set of scripts to build ASiMoV-CCS dependencies on various systems.

## Installation Options

This repository provides two methods for installing dependencies:

1. Legacy Bash scripts (original method)
2. New Python-based installation (recommended)

## Python-based Installation (Recommended)

### Prerequisites

- Python 3.7 or higher
- Git
- Core development tools (compilers, build tools)

### Setup with Poetry (Recommended)

[Poetry](https://python-poetry.org/) is used for Python dependency management. It simplifies package installation and virtual environment creation.

1. Install Poetry if you don't have it already:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies using Poetry:

```bash
# Install dependencies
poetry install

# Run the installation script using Poetry
poetry run ccs-install --env gnu_macos

# Configure environment for building CCS
eval $(poetry run ccs-setup --env gnu_macos)
```

### Alternative Setup (without Poetry)

1. Install required Python packages:

```bash
pip install -r requirements.txt
```

2. Run the installation script:

```bash
# Install all dependencies for the detected environment
./install.py

# Specify environment explicitly
./install.py --env gnu_macos

# Install specific dependencies
./install.py --dependencies hdf5,petsc

# Set custom install and build directories
./install.py --install-dir ~/ccs-deps --build-dir /tmp/build-ccs-deps
```

3. Source the environment for building CCS:

```bash
# Generate and apply environment variables
eval $(./setup.py)

# Or export to a file
./setup.py > env.sh
source env.sh
```

### Configuration

The Python installation uses YAML configuration files in the `config` directory:

- `config/default_config.yml` - Default configuration for all environments
- `config/gnu_macos.yml` - macOS-specific configuration
- `config/gnu_ubuntu.yml` - Ubuntu-specific configuration
- `config/cray_A2.yml` - Cray A2-specific configuration

You can create custom configurations and specify them with the `--config` flag:

```bash
poetry run ccs-install --config my_custom_config.yml
# or
./install.py --config my_custom_config.yml
```

## For Developers

If you're developing or extending the CCS Dependencies tool, Poetry provides a convenient development environment:

```bash
# Create a development environment
poetry shell

# Run the installation script directly
ccs-install --env gnu_macos --debug

# Format code with black
poetry run black .

# Run linting
poetry run pylint installers utils
```

## Legacy Bash Installation

### Setup

1. Set up the `INSTALL_DIR` and `BUILD_DIR` variables in `setup_base.sh`:

```bash
INSTALL_DIR=$HOME/ccs-libs
BUILD_DIR=/tmp/build-ccs-deps/
```

2. Build and install the dependencies:

```bash
ENV=cray_A2 ./install_base.sh
```

Set ENV according to your platform and desired build environment. The possible values each have a file named `setup_$ENV.sh` in the root folder of this repo.

## Building CCS

Once all the libraries have been installed, source the right setup script to build CCS:

### With Python setup:

```bash
# With Poetry
eval $(poetry run ccs-setup --env gnu_macos)

# Without Poetry
eval $(./setup.py --env gnu_macos)

# Then clone and build CCS
git clone git@github.com:asimovpp/asimov-ccs.git
cd asimov-ccs
make all
```

### With legacy Bash setup:

```bash
source setup_cray_A2.sh

git clone git@github.com:asimovpp/asimov-ccs.git
cd asimov-ccs
make all
```

## Available Dependencies

The following dependencies can be installed:

- makedepf90 - Fortran dependency generator
- fyaml_c - YAML parser in C
- hdf5 - Hierarchical Data Format library
- adios2 - Adaptable I/O System for scientific data
- petsc - Portable, Extensible Toolkit for Scientific Computation
- parhip - Parallel High-quality Graph Partitioning
- parmetis - Parallel Graph Partitioning and Fill-reducing Matrix Ordering
- rcm_f90 - Reverse Cuthill-McKee algorithm in Fortran 90
- python_deps - Python dependencies (PyYAML, LIT, etc.)