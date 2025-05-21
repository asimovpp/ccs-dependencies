#!/usr/bin/env python3
"""
System detection utilities for CCS dependencies
"""
import platform
import os
import logging
from pathlib import Path


def detect_system():
    """
    Detect system and return appropriate environment name
    
    Returns:
        str: Environment name (e.g., gnu_ubuntu, gnu_macos)
    """
    system = platform.system().lower()
    
    if system == "darwin":
        # macOS detection
        return "gnu_macos"
    elif system == "linux":
        # Linux distribution detection
        try:
            import distro
            distname = distro.id().lower()
        except ImportError:
            # Fallback if distro module is not available
            os_release_path = Path("/etc/os-release")
            if os_release_path.exists():
                with os_release_path.open() as f:
                    for line in f:
                        if line.startswith("ID="):
                            distname = line.split("=")[1].strip().strip('"').lower()
                            break
            else:
                distname = "unknown"
        
        # Check for specific distributions
        if distname in ["ubuntu", "debian"]:
            return "gnu_ubuntu"
        elif "cray" in platform.version().lower() or Path("/opt/cray").exists():
            return "cray_A2"
    
    # Default to gnu_ubuntu if we can't determine the system
    logging.warning(f"Could not determine system type, defaulting to gnu_ubuntu")
    return "gnu_ubuntu"


def get_cpu_count():
    """
    Get number of CPU cores
    
    Returns:
        int: Number of CPU cores
    """
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        # Fallback if multiprocessing is not available
        return 4  # Conservative default