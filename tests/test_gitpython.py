#!/usr/bin/env python3
"""
Test script for GitPython integration
"""
import shutil
import tempfile
import logging
from pathlib import Path
from ccs_dep.utils.command import clone_repository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def test_clone_repository():
    """
    Test the clone_repository function with GitPython
    """
    # Create a temporary directory for the test
    temp_dir = Path(tempfile.mkdtemp())
    try:
        logging.info(f"Testing clone_repository in {temp_dir}")
        
        # Clone a small repository (demo repository)
        success = clone_repository(
            url="https://github.com/octocat/Hello-World.git",
            directory=temp_dir,
            depth=1
        )
        
        # Verify the repository was cloned successfully
        logging.info("Repository cloned successfully")
        assert success, "Clone operation failed"
        
        # Check if the repository was cloned correctly
        git_dir = temp_dir / ".git"
        if git_dir.is_dir():
            logging.info("Git directory exists, clone successful!")
        else:
            logging.error("Git directory doesn't exist, clone failed")
            assert False, "Git directory doesn't exist after clone"
    finally:
        # Clean up the temporary directory
        logging.info(f"Cleaning up temporary directory {temp_dir}")
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    try:
        test_clone_repository()
        print("Test result: PASSED")
        exit(0)
    except AssertionError as e:
        print(f"Test result: FAILED - {e}")
        exit(1)