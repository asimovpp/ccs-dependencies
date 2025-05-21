#!/usr/bin/env python3
"""
HDF5 installer for CCS dependencies
"""
import os
import logging
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command, clone_repository


class Hdf5Installer(BaseInstaller):
    """
    HDF5 installer
    """
    def download(self):
        """
        Download HDF5 source code
        """
        logging.info(f"Downloading HDF5 version {self.version}")
        build_dir = Path(self.build_dir)
        os.chdir(build_dir)
        
        # Clone HDF5 repository
        source_dir = Path(self.source_dir)
        clone_repository(
            url="https://github.com/HDFGroup/hdf5.git",
            directory=source_dir,
            branch=f"hdf5_{self.version}",
            depth=1
        )
    
    def configure(self):
        """
        Configure HDF5 build
        """
        logging.info("Configuring HDF5")
        source_dir = Path(self.source_dir)
        os.chdir(source_dir)
        
        # Get configure options from config
        configure_options = self.dep_config.get("configure_options", [])
        
        # Convert install dir to Path and get string representation
        install_dir = Path(self.dep_install_dir)
        
        # Build configure command
        cmd = ["./configure", "--enable-parallel", f"--prefix={str(install_dir)}"]
        cmd.extend(configure_options)
        
        # Run configure
        run_command(cmd)
    
    def build(self):
        """
        Build HDF5
        """
        logging.info("Building HDF5")
        source_dir = Path(self.source_dir)
        os.chdir(str(source_dir))
        
        # Run make
        run_command(["make", f"-j{self.parallel_jobs}"])
    
    def install(self):
        """
        Install HDF5
        """
        logging.info("Installing HDF5")
        source_dir = Path(self.source_dir)
        os.chdir(source_dir)
        
        # Run make install
        run_command(["make", "install"])