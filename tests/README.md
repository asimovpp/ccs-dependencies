# CCS Dependencies Tests

This directory contains tests for the CCS Dependencies installers and utilities. The tests are designed to be completely ephemeral, running in isolated sandboxes that are cleaned up after each test run.

## Test Organization

- `test_installers_base.py` - Base test class with common functionality for installer tests
- `test_hdf5_installer.py` - Tests for the HDF5 installer
- `test_parmetis_installer.py` - Tests for the ParMETIS installer
- `test_petsc_installer.py` - Tests for the PETSc installer
- `test_gitpython.py` - Tests for the GitPython integration
- `run_installer_tests.py` - Script to run all installer tests

## Running Tests

You can run the tests using pytest or the provided test runner script:

```bash
# Run all tests
poetry run pytest

# Run a specific test file
poetry run pytest tests/test_hdf5_installer.py

# Run tests with more detailed output
poetry run pytest -xvs tests/

# Run tests with the test runner script
poetry run python tests/run_installer_tests.py
```

## Test Design

The tests are designed with the following principles:

1. **Isolation**: Each test runs in its own temporary directory
2. **Mock External Dependencies**: Git operations and command execution are mocked
3. **Complete Cleanup**: All temporary resources are removed after each test
4. **No Side Effects**: Tests do not perform actual installations or modifications
5. **Comprehensive Coverage**: Each installer method is tested separately

## Adding New Tests

To add tests for a new installer:

1. Create a new test file in the `tests/` directory named `test_<installer_name>_installer.py`
2. Extend the `BaseInstallerTest` class to inherit common setup and teardown functionality
3. Implement test methods for each phase of installation (prepare, download, configure, build, install)
4. Update `run_installer_tests.py` to include the new test file

## Testing Dependencies

The following dependencies are required for testing:

- `pytest` - Testing framework
- `pytest-mock` - For creating mocks and patching functions
- `coverage` - For measuring test coverage (optional)

These are automatically installed as development dependencies when using Poetry.