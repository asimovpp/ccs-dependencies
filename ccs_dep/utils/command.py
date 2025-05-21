#!/usr/bin/env python3
"""
Command execution utilities for CCS dependencies
"""
import subprocess
import logging
import os
import sys
from pathlib import Path
from git import Repo, GitCommandError


def run_command(cmd, cwd=None, env=None, check=True, capture_output=False):
    """
    Run a command and return the result
    
    Args:
        cmd (list): Command to run
        cwd (str, optional): Working directory
        env (dict, optional): Environment variables
        check (bool, optional): Check return code
        capture_output (bool, optional): Capture output
        
    Returns:
        str: Command output if capture_output is True, otherwise None
        
    Raises:
        subprocess.CalledProcessError: If check is True and the command returns non-zero
    """
    cmd_str = " ".join(cmd)
    logging.debug(f"Running command: {cmd_str}")
    
    if env is None:
        env = os.environ.copy()
    
    try:
        if capture_output:
            result = subprocess.run(
                cmd, 
                cwd=cwd, 
                env=env, 
                check=check,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout
        else:
            subprocess.run(cmd, cwd=cwd, env=env, check=check)
            return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {cmd_str}")
        if e.stdout:
            logging.error(f"Standard output: {e.stdout}")
        if e.stderr:
            logging.error(f"Standard error: {e.stderr}")
        if check:
            raise
        return None
    except Exception as e:
        logging.error(f"Error running command: {cmd_str}")
        logging.error(f"Error: {e}")
        raise


def apply_patch(patch_file, cwd=None):
    """
    Apply a patch file
    
    Args:
        patch_file (str or Path): Path to patch file
        cwd (str or Path, optional): Working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    patch_path = Path(patch_file) if not isinstance(patch_file, Path) else patch_file
    logging.info(f"Applying patch: {patch_path}")
    try:
        run_command(["patch", "-p1", "-i", str(patch_path)], cwd=cwd)
        return True
    except Exception as e:
        logging.error(f"Error applying patch: {e}")
        return False


def clone_repository(url, directory, branch=None, depth=1):
    """
    Clone a Git repository using GitPython
    
    Args:
        url (str): Repository URL
        directory (str or Path): Directory to clone into
        branch (str, optional): Branch to clone
        depth (int, optional): Clone depth
        
    Returns:
        bool: True if successful, False otherwise
    """
    logging.info(f"Cloning repository: {url}")
    
    # Convert to Path object if it's not already
    target_dir = Path(directory) if not isinstance(directory, Path) else directory
    
    # Prepare clone options
    clone_args = {}
    
    if depth:
        clone_args['depth'] = depth
    
    if branch:
        clone_args['branch'] = branch
    
    try:
        # Clone the repository using GitPython
        repo = Repo.clone_from(url, str(target_dir), **clone_args)
        logging.info(f"Repository cloned successfully to {repo.working_dir}")
        return True
    except GitCommandError as e:
        logging.error(f"Git command error while cloning repository: {e}")
        return False
    except Exception as e:
        logging.error(f"Error cloning repository: {e}")
        return False


def download_file(url, output_file):
    """
    Download a file
    
    Args:
        url (str): URL to download
        output_file (str or Path): Output file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Convert to Path object if it's not already
    output_path = Path(output_file) if not isinstance(output_file, Path) else output_file
    
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Try wget first
        try:
            run_command(["wget", "-O", str(output_path), url])
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try curl as fallback
            try:
                run_command(["curl", "-L", "-o", str(output_path), url])
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Use Python as final fallback
                import urllib.request
                urllib.request.urlretrieve(url, str(output_path))
                return True
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return False


def extract_archive(archive_file, destination=None):
    """
    Extract an archive file
    
    Args:
        archive_file (str or Path): Archive file path
        destination (str or Path, optional): Destination directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Convert to Path objects if they're not already
    archive_path = Path(archive_file) if not isinstance(archive_file, Path) else archive_file
    
    if not destination:
        dest_path = archive_path.parent
    else:
        dest_path = Path(destination) if not isinstance(destination, Path) else destination
    
    # Ensure destination directory exists
    dest_path.mkdir(parents=True, exist_ok=True)
    
    try:
        archive_str = str(archive_path)
        dest_str = str(dest_path)
        
        if archive_str.endswith(".tar.gz") or archive_str.endswith(".tgz"):
            run_command(["tar", "-xzf", archive_str, "-C", dest_str])
        elif archive_str.endswith(".tar.bz2") or archive_str.endswith(".tbz2"):
            run_command(["tar", "-xjf", archive_str, "-C", dest_str])
        elif archive_str.endswith(".tar"):
            run_command(["tar", "-xf", archive_str, "-C", dest_str])
        elif archive_str.endswith(".zip"):
            run_command(["unzip", "-q", archive_str, "-d", dest_str])
        else:
            logging.error(f"Unsupported archive format: {archive_path}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error extracting archive: {e}")
        return False