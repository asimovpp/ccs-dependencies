#!/usr/bin/env python3
"""
HDF5 installer for CCS dependencies
"""
import os
import logging
from installers.base import BaseInstaller
from utils.command import run_command, clone_repository


class Hdf5Installer(BaseInstaller):
    """
    HDF5 installer
    """
    def download(self):
        """
        Download HDF5 source code
        """
        logging.info(f"Downloading HDF5 version {self.version}")
        os.chdir(self.build_dir)
        
        # Clone HDF5 repository
        clone_repository(
            url="https://github.com/HDFGroup/hdf5.git",
            branch=f"hdf5_{self.version}",
            depth=1
        )
    
    def configure(self):
        """
        Configure HDF5 build
        """
        logging.info("Configuring HDF5")
        os.chdir(self.source_dir)
        
        # Get configure options from config
        configure_options = self.dep_config.get("configure_options", [])
        
        # Build configure command
        cmd = ["./configure", "--enable-parallel", f"--prefix={self.dep_install_dir}"]
        cmd.extend(configure_options)
        
        # Run configure
        run_command(cmd)
    
    def build(self):
        """
        Build HDF5
        """
        logging.info("Building HDF5")
        os.chdir(self.source_dir)
        
        # Run make
        run_command(["make", f"-j{self.parallel_jobs}"])
    
    def install(self):
        """
        Install HDF5
        """
        logging.info("Installing HDF5")
        os.chdir(self.source_dir)
        
        # Run make install
        run_command(["make", "install"])