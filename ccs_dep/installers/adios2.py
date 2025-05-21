#!/usr/bin/env python3
"""
ADIOS2 installer for CCS dependencies
"""
import os
import logging
import shutil
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command, clone_repository


class Adios2Installer(BaseInstaller):
    """
    ADIOS2 installer

    ADIOS2 (Adaptable Input Output System) is a framework for scientific data I/O.
    """
    
    def __init__(self, config, env):
        """
        Initialize the ADIOS2 installer
        
        Args:
            config (dict): Configuration dictionary
            env (Environment): Environment object
        """
        super().__init__(config, env)
        
        # Check if we need to update the version
        if not self.version and "ADIOS2_VERSION" in self.env_vars:
            self.version = self.env_vars.get("ADIOS2_VERSION")
            
        # Check if we need to update the installation directory
        if not self.dep_install_dir and "ADIOS2" in self.env_vars:
            self.dep_install_dir = self.env_vars.get("ADIOS2")
            
    def download(self):
        """
        Download ADIOS2 source code
        """
        logging.info(f"Downloading ADIOS2 version {self.version}")
        os.chdir(self.build_dir)
        
        # Clone ADIOS2 repository
        source_dir = Path(self.source_dir)
        clone_repository(
            url="https://github.com/ornladios/ADIOS2.git",
            directory=source_dir,
            branch=f"v{self.version}",
            depth=1
        )
    
    def configure(self):
        """
        Configure ADIOS2 build
        """
        logging.info("Configuring ADIOS2")
        source_dir = Path(self.source_dir)
        
        # Create build directory
        build_dir = source_dir / "build"
        build_dir.mkdir(exist_ok=True)
        os.chdir(build_dir)
        
        # Get compiler variables
        cc = self.env_vars.get("CC", "mpicc")
        cxx = self.env_vars.get("CXX", "mpicxx")
        fc = self.env_vars.get("FC", "mpifort")
        hdf5_root = self.env_vars.get("HDF5_ROOT", "")
        
        # Run CMake configuration
        cmake_args = [
            "cmake",
            f"-DCMAKE_C_COMPILER={cc}",
            f"-DCMAKE_CXX_COMPILER={cxx}",
            f"-DCMAKE_Fortran_COMPILER={fc}",
            "-DADIOS2_USE_SST=OFF",
            "-DADIOS2_USE_Fortran=ON",
            "-DADIOS2_USE_MPI=ON",
            "-DADIOS2_USE_HDF5=ON",
            f"-DHDF5_ROOT={hdf5_root}",
            "-DADIOS2_USE_Python=OFF",
            "-DADIOS2_USE_ZeroMQ=OFF",
            "-DBUILD_SHARED_LIBS=ON",
            f"-DCMAKE_INSTALL_PREFIX={self.dep_install_dir}",
            ".."
        ]
        
        run_command(cmake_args)
    
    def build(self):
        """
        Build ADIOS2
        """
        logging.info("Building ADIOS2")
        source_dir = Path(self.source_dir)
        build_dir = source_dir / "build"
        os.chdir(build_dir)
        
        # Run make with parallel jobs
        run_command(["make", f"-j", str(self.parallel_jobs)])
    
    def install(self):
        """
        Install ADIOS2
        """
        logging.info("Installing ADIOS2")
        source_dir = Path(self.source_dir)
        build_dir = source_dir / "build"
        os.chdir(build_dir)
        
        # Run make install
        run_command(["make", "install"])