#!/usr/bin/env python3
"""
Command execution utilities for CCS dependencies
"""
import subprocess
import logging
import os
import sys


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
        patch_file (str): Path to patch file
        cwd (str, optional): Working directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    logging.info(f"Applying patch: {patch_file}")
    try:
        run_command(["patch", "-p1", "-i", patch_file], cwd=cwd)
        return True
    except Exception as e:
        logging.error(f"Error applying patch: {e}")
        return False


def clone_repository(url, directory=None, branch=None, depth=1):
    """
    Clone a Git repository
    
    Args:
        url (str): Repository URL
        directory (str, optional): Directory to clone into
        branch (str, optional): Branch to clone
        depth (int, optional): Clone depth
        
    Returns:
        bool: True if successful, False otherwise
    """
    cmd = ["git", "clone"]
    
    if depth:
        cmd.extend(["--depth", str(depth)])
    
    if branch:
        cmd.extend(["--branch", branch])
    
    cmd.append(url)
    
    if directory:
        cmd.append(directory)
    
    try:
        run_command(cmd)
        return True
    except Exception as e:
        logging.error(f"Error cloning repository: {e}")
        return False


def download_file(url, output_file):
    """
    Download a file
    
    Args:
        url (str): URL to download
        output_file (str): Output file path
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Try wget first
        try:
            run_command(["wget", "-O", output_file, url])
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try curl as fallback
            try:
                run_command(["curl", "-L", "-o", output_file, url])
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Use Python as final fallback
                import urllib.request
                urllib.request.urlretrieve(url, output_file)
                return True
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return False


def extract_archive(archive_file, destination=None):
    """
    Extract an archive file
    
    Args:
        archive_file (str): Archive file path
        destination (str, optional): Destination directory
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not destination:
        destination = os.path.dirname(archive_file)
    
    try:
        if archive_file.endswith(".tar.gz") or archive_file.endswith(".tgz"):
            run_command(["tar", "-xzf", archive_file, "-C", destination])
        elif archive_file.endswith(".tar.bz2") or archive_file.endswith(".tbz2"):
            run_command(["tar", "-xjf", archive_file, "-C", destination])
        elif archive_file.endswith(".tar"):
            run_command(["tar", "-xf", archive_file, "-C", destination])
        elif archive_file.endswith(".zip"):
            run_command(["unzip", "-q", archive_file, "-d", destination])
        else:
            logging.error(f"Unsupported archive format: {archive_file}")
            return False
        return True
    except Exception as e:
        logging.error(f"Error extracting archive: {e}")
        return False