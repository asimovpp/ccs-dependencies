#!/usr/bin/env python3
"""
Main test runner for installer tests
"""
import os
import sys
import pytest
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def main():
    """
    Run all installer tests
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    # Determine the test directory
    test_dir = Path(__file__).parent
    
    # Print test information
    logging.info("Running installer tests")
    logging.info(f"Test directory: {test_dir}")
    
    # Run the tests
    test_files = [
        "test_adios2_installer.py",
        "test_fyaml_c_installer.py",
        "test_hdf5_installer.py",
        "test_makedepf90_installer.py",
        "test_parhip_installer.py",
        "test_parmetis_installer.py",
        "test_petsc_installer.py",
        "test_python_deps_installer.py",
        "test_rcm_f90_installer.py"
    ]
    
    test_paths = [str(test_dir / test_file) for test_file in test_files]
    
    # Add arguments for verbose output and coverage
    args = [
        "-v",                      # Verbose output
        "--no-header",             # No header
        "--no-summary",            # No summary
        "-xvs",                    # Exit on first failure, verbose, short output
    ]
    
    # Run pytest programmatically
    exit_code = pytest.main(args + test_paths)
    
    # Log results
    if exit_code == 0:
        logging.info("All tests passed successfully!")
    else:
        logging.error(f"Tests failed with exit code: {exit_code}")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())