#!/usr/bin/env python3
"""
Base test class for installer tests
"""
import os
import tempfile
import shutil
import logging
from pathlib import Path
import pytest


class BaseInstallerTest:
    """
    Base class for installer tests
    Provides common setup and teardown methods for all installer tests
    """
    
    @pytest.fixture(autouse=True)
    def setup_test(self, monkeypatch):
        """
        Setup test environment with temporary directories
        
        Args:
            monkeypatch: pytest monkeypatch fixture
        """
        # Configure logging for tests
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Create temporary directories for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.build_dir = self.temp_dir / "build"
        self.install_dir = self.temp_dir / "install"
        self.build_dir.mkdir()
        self.install_dir.mkdir()
        
        # Store original directory to return to after test
        self.original_dir = Path.cwd()
        
        # Set environment variables for testing
        monkeypatch.setenv("BUILD_DIR", str(self.build_dir))
        monkeypatch.setenv("INSTALL_DIR", str(self.install_dir))
        
        # Create a mock environment class
        class MockEnvironment:
            def __init__(self, env_vars):
                self.env_vars = env_vars
            
            def get_env_vars(self):
                return self.env_vars
        
        # Create base environment variables
        self.env_vars = {
            "BUILD_DIR": str(self.build_dir),
            "INSTALL_DIR": str(self.install_dir),
            "CC": "mpicc",
            "CXX": "mpicxx",
            "FC": "mpifort",
            "CMP": "gnu"
        }
        
        # Create mock environment
        self.env = MockEnvironment(self.env_vars)
        
        # Create base configuration
        self.config = {
            "parallel_jobs": 2,  # Use minimal parallel jobs for tests
            "dependencies": {}
        }
        
        yield
        
        # Change back to original directory
        os.chdir(self.original_dir)
        
        # Clean up temporary directories
        shutil.rmtree(self.temp_dir)
    
    def mock_command_success(self, cmd, cwd=None, env=None, check=True, capture_output=False):
        """
        Mock for run_command that always succeeds
        
        Args:
            cmd: Command to run
            cwd: Working directory
            env: Environment variables
            check: Check return code
            capture_output: Capture output
            
        Returns:
            str: Empty string if capture_output is True, otherwise None
        """
        logging.info(f"Mock command: {' '.join(cmd)}")
        return "" if capture_output else None
    
    def mock_clone_success(self, url, directory, branch=None, depth=1):
        """
        Mock for clone_repository that always succeeds
        
        Args:
            url: Repository URL
            directory: Directory to clone into
            branch: Branch to clone
            depth: Clone depth
            
        Returns:
            bool: True
        """
        logging.info(f"Mock clone: {url} -> {directory}")
        # Create the directory to simulate successful clone
        Path(directory).mkdir(parents=True, exist_ok=True)
        # Create a .git directory to simulate a git repository
        git_dir = Path(directory) / ".git"
        git_dir.mkdir(exist_ok=True)
        return True
    
    def mock_apply_patch_success(self, patch_file, cwd=None):
        """
        Mock for apply_patch that always succeeds
        
        Args:
            patch_file: Patch file
            cwd: Working directory
            
        Returns:
            bool: True
        """
        logging.info(f"Mock apply patch: {patch_file}")
        return True
    
    def create_test_file(self, path, content=""):
        """
        Create a test file with given content
        
        Args:
            path: Path to file
            content: File content
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        
    def assert_directory_exists(self, path):
        """
        Assert that directory exists
        
        Args:
            path: Path to directory
        """
        assert Path(path).exists(), f"Directory {path} does not exist"
        assert Path(path).is_dir(), f"{path} is not a directory"
    
    def assert_file_exists(self, path):
        """
        Assert that file exists
        
        Args:
            path: Path to file
        """
        assert Path(path).exists(), f"File {path} does not exist"
        assert Path(path).is_file(), f"{path} is not a file"