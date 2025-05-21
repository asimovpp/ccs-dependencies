#!/usr/bin/env python3
"""
RCM-f90 installer for CCS dependencies
"""
import os
import logging
import shutil
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command, clone_repository


class RcmF90Installer(BaseInstaller):
    """
    RCM-f90 installer

    RCM-f90 is a Fortran 90 implementation of the Reverse Cuthill-McKee algorithm
    for bandwidth reduction of sparse matrices.
    """
    
    def __init__(self, config, env):
        """
        Initialize the RCM-f90 installer
        
        Args:
            config (dict): Configuration dictionary
            env (Environment): Environment object
        """
        super().__init__(config, env)
        # Override the name determined from the class name to match the expected format
        self.name = "rcm_f90"
        
        # Check if we need to update the version
        if not self.version and "RCM_F90_VERSION" in self.env_vars:
            self.version = self.env_vars.get("RCM_F90_VERSION")
            
        # Check if we need to update the installation directory
        if not self.dep_install_dir and "RCMF90" in self.env_vars:
            self.dep_install_dir = self.env_vars.get("RCMF90")
    
    def download(self):
        """
        Download RCM-f90 source code
        """
        logging.info("Downloading RCM-f90")
        os.chdir(self.build_dir)
        
        # Clone RCM-f90 repository
        source_dir = Path(self.source_dir)
        clone_repository(
            url="https://github.com/asimovpp/RCM-f90.git",
            directory=source_dir,
            depth=1
        )
    
    def configure(self):
        """
        No separate configure step for RCM-f90
        """
        pass
    
    def build(self):
        """
        Build RCM-f90
        """
        logging.info("Building RCM-f90")
        source_dir = Path(self.source_dir)
        os.chdir(source_dir)
        
        # Extract compiler type from environment
        compiler_type = self.env_vars.get("CMP", "gnu")
        if "_" in compiler_type:
            # Handle compiler names like "gnu_ubuntu" -> "gnu"
            compiler_type = compiler_type.split("_")[0]
        
        # Run make
        run_command(["make", f"CMP={compiler_type}"])
    
    def install(self):
        """
        Install RCM-f90
        """
        logging.info("Installing RCM-f90")
        source_dir = Path(self.source_dir)
        install_dir = Path(self.dep_install_dir)
        
        # Create installation directories
        install_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy library and include files
        lib_dir = source_dir / "lib"
        include_dir = source_dir / "include"
        
        if lib_dir.exists():
            dest_lib_dir = install_dir / "lib"
            if dest_lib_dir.exists():
                shutil.rmtree(dest_lib_dir)
            shutil.copytree(lib_dir, dest_lib_dir)
        
        if include_dir.exists():
            dest_include_dir = install_dir / "include"
            if dest_include_dir.exists():
                shutil.rmtree(dest_include_dir)
            shutil.copytree(include_dir, dest_include_dir)