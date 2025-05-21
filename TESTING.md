# Testing the Python-based Installation

This document provides steps for testing the Python-based dependency installation on different platforms.

## Testing on macOS

1. **Prepare the Environment**

   Ensure you have the necessary prerequisites:
   
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install MPI and other dependencies
   brew install open-mpi cmake
   
   # Install Python packages
   pip install -r requirements.txt
   ```

2. **Verify System Detection**

   ```bash
   # Run with debug output
   ./install.py --debug
   
   # Check that the system is detected correctly
   # The output should include: "Detected environment: gnu_macos"
   ```

3. **Test Individual Dependency Installation**

   ```bash
   # Test with a simple dependency first
   ./install.py --dependencies makedepf90 --debug
   
   # Verify installation
   ls -la $(./setup.py --format json | python -c "import sys, json; print(json.load(sys.stdin)['MAKEDEPF90'])")
   ```

4. **Test Environment Variable Setup**

   ```bash
   # Generate environment variables
   ./setup.py
   
   # Store environment in a file
   ./setup.py > env_test.sh
   
   # Source the environment
   source env_test.sh
   
   # Verify environment variables are set
   echo $PETSC_DIR
   echo $HDF5_ROOT
   ```

5. **Build All Dependencies**

   ```bash
   # Full installation
   ./install.py --env gnu_macos
   
   # Verify success by checking installation summary
   ```

## Testing on Ubuntu (or WSL)

1. **Prepare the Environment**

   ```bash
   # Update system packages
   sudo apt update
   
   # Install required packages
   sudo apt install git cmake make gcc g++ gfortran openmpi-bin libopenmpi-dev
   
   # Install Python packages
   pip install -r requirements.txt
   ```

2. **Follow the same testing steps as for macOS**

   The detection should correctly identify "gnu_ubuntu" as the environment.

## Testing on Cray Systems

If you have access to a Cray system:

1. **Load Modules**

   ```bash
   # Load necessary modules (system-specific)
   module load PrgEnv-cray
   module load cray-mpich
   ```

2. **Verify System Detection and Installation**

   Follow similar steps as above, ensuring the system is detected as "cray_A2".

## Troubleshooting

If issues occur during testing:

1. **Configuration Problems**

   - Check the YAML configuration files in `config/`
   - Ensure compiler variables are set correctly
   - Verify install and build directories have write permissions

2. **Dependency Problems**

   - Inspect logs for detailed error messages
   - Retry failed dependencies individually with `--debug` flag

3. **Environment Issues**

   - Confirm MPI is installed and working
   - Test compiler availability with `which mpicc`, `which mpicxx`, etc.
   - For library path issues, check if LD_LIBRARY_PATH is being set correctly