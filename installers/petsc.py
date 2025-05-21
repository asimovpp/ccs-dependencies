#!/usr/bin/env python3
"""
PETSc installer for CCS dependencies
"""
import os
import logging
from installers.base import BaseInstaller
from utils.command import run_command, clone_repository


class PetscInstaller(BaseInstaller):
    """
    PETSc installer
    """
    def download(self):
        """
        Download PETSc source code
        """
        logging.info(f"Downloading PETSc version {self.version}")
        os.chdir(self.build_dir)
        
        # Clone PETSc repository
        clone_repository(
            url="https://github.com/petsc/petsc.git",
            branch=f"v{self.version}",
            depth=1
        )
        
        # Set PETSC_DIR environment variable
        os.environ["PETSC_DIR"] = self.source_dir
    
    def configure(self):
        """
        Configure PETSc build
        """
        logging.info("Configuring PETSc")
        os.chdir(self.source_dir)
        
        # Get compiler variables
        cc = self.env_vars.get("CC", "mpicc")
        cxx = self.env_vars.get("CXX", "mpicxx")
        fc = self.env_vars.get("FC", "mpifort")
        
        # Get configure options from config
        configure_options = self.dep_config.get("configure_options", [
            "--download-fblaslapack=yes",
            "--with-fortran-datatypes=1",
            "--with-fortran-interfaces=1",
            "--with-fortran-bindings=1",
            "--with-fortran-kernels=1",
            "--with-debugging=1"
        ])
        
        # Build configure command
        cmd = [
            "./configure",
            f"--with-cc={cc}",
            f"--with-cxx={cxx}",
            f"--with-fc={fc}",
            f"--prefix={self.dep_install_dir}"
        ]
        cmd.extend(configure_options)
        
        # Run configure
        run_command(cmd)
    
    def build(self):
        """
        Build PETSc
        """
        logging.info("Building PETSc")
        os.chdir(self.source_dir)
        
        # Run make
        run_command(["make", f"-j{self.parallel_jobs}"])
    
    def install(self):
        """
        Install PETSc
        """
        logging.info("Installing PETSc")
        os.chdir(self.source_dir)
        
        # Run make install
        run_command(["make", "install"])