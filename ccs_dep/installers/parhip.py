#!/usr/bin/env python3
"""
ParHIP installer for CCS dependencies
"""
import os
import logging
import shutil
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command, clone_repository


class ParhipInstaller(BaseInstaller):
    """
    ParHIP installer

    ParHIP is a parallel high quality graph partitioning tool.
    """
    
    def __init__(self, config, env):
        """
        Initialize the ParHIP installer
        
        Args:
            config (dict): Configuration dictionary
            env (Environment): Environment object
        """
        super().__init__(config, env)
        
        # Check if we need to update the version
        if not self.version and "PARHIP_VERSION" in self.env_vars:
            self.version = self.env_vars.get("PARHIP_VERSION")
            
        # Check if we need to update the installation directory
        if not self.dep_install_dir and "PARHIP" in self.env_vars:
            self.dep_install_dir = self.env_vars.get("PARHIP")
            
    def download(self):
        """
        Download ParHIP source code
        """
        logging.info(f"Downloading ParHIP version {self.version}")
        os.chdir(self.build_dir)
        
        # Clone ParHIP repository (KaHIP)
        source_dir = Path(self.source_dir)
        clone_repository(
            url="https://github.com/KaHIP/KaHIP.git",
            directory=source_dir,
            branch=f"v{self.version}",
            depth=1
        )
    
    def configure(self):
        """
        Configure ParHIP build
        """
        logging.info("Configuring ParHIP")
        source_dir = Path(self.source_dir)
        
        # Create build directory
        build_dir = source_dir / "build"
        build_dir.mkdir(exist_ok=True)
        os.chdir(build_dir)
        
        # Get compiler variables
        cc = self.env_vars.get("CC", "mpicc")
        
        # Setup environment variables for cmake
        env_vars = os.environ.copy()
        env_vars["CC"] = cc
        
        # Run CMake configuration
        cmake_args = [
            "cmake",
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DCMAKE_INSTALL_PREFIX={self.dep_install_dir}",
            ".."
        ]
        
        run_command(cmake_args, env=env_vars)
    
    def build(self):
        """
        Build ParHIP
        """
        logging.info("Building ParHIP")
        source_dir = Path(self.source_dir)
        build_dir = source_dir / "build"
        os.chdir(build_dir)
        
        # Run make with parallel jobs
        run_command(["make", f"-j", str(self.parallel_jobs)])
    
    def install(self):
        """
        Install ParHIP
        """
        logging.info("Installing ParHIP")
        source_dir = Path(self.source_dir)
        build_dir = source_dir / "build"
        os.chdir(build_dir)
        
        # Run make install
        run_command(["make", "install"])