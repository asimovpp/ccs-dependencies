#!/usr/bin/env python3
"""
Makedepf90 installer for CCS dependencies
"""
import os
import logging
import shutil
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command, clone_repository


class Makedepf90Installer(BaseInstaller):
    """
    Makedepf90 installer

    Makedepf90 is a tool to generate Fortran 90 dependencies for makefiles.
    """
    
    def __init__(self, config, env):
        """
        Initialize the Makedepf90 installer
        
        Args:
            config (dict): Configuration dictionary
            env (Environment): Environment object
        """
        super().__init__(config, env)
        
        # Check if we need to update the installation directory
        if not self.dep_install_dir and "MAKEDEPF90" in self.env_vars:
            self.dep_install_dir = self.env_vars.get("MAKEDEPF90")
            
    def download(self):
        """
        Download Makedepf90 source code
        """
        logging.info("Downloading Makedepf90")
        os.chdir(self.build_dir)
        
        # Clone Makedepf90 repository
        source_dir = Path(self.source_dir)
        clone_repository(
            url="https://salsa.debian.org/science-team/makedepf90.git",
            directory=source_dir
        )
    
    def configure(self):
        """
        Configure Makedepf90 build
        """
        logging.info("Configuring Makedepf90")
        source_dir = Path(self.source_dir)
        os.chdir(source_dir)
        
        # Run configure script
        run_command([
            "./configure", 
            f"--prefix={self.dep_install_dir}"
        ])
    
    def build(self):
        """
        Build Makedepf90
        """
        logging.info("Building Makedepf90")
        source_dir = Path(self.source_dir)
        os.chdir(source_dir)
        
        # Run make
        run_command(["make"])
    
    def install(self):
        """
        Install Makedepf90
        
        Note: The original script doesn't use 'make install' but copies the binary directly
        """
        logging.info("Installing Makedepf90")
        source_dir = Path(self.source_dir)
        
        # Create bin directory in installation path
        bin_dir = Path(self.dep_install_dir) / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy makedepf90 binary to installation directory
        makedepf90_bin = source_dir / "makedepf90"
        if makedepf90_bin.exists():
            shutil.copy2(makedepf90_bin, bin_dir)
        else:
            raise FileNotFoundError(f"Makedepf90 binary not found at {makedepf90_bin}")