#!/usr/bin/env python3
"""
ParMETIS installer for CCS dependencies
"""
import os
import logging
import shutil
from installers.base import BaseInstaller
from utils.command import run_command, clone_repository, apply_patch


class ParmetisInstaller(BaseInstaller):
    """
    ParMETIS installer
    """
    def prepare(self):
        """
        Prepare build environment
        """
        super().prepare()
        
        # Create a subdirectory for ParMETIS and its dependencies
        self.parmetis_dir = os.path.join(self.build_dir, "parmetis")
        os.makedirs(self.parmetis_dir, exist_ok=True)
        
        # Copy patch file if needed
        patch_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "patch")
        self.patch_file = os.path.join(self.build_dir, "gklib_force_fpic.patch")
        shutil.copy(
            os.path.join(patch_dir, "gklib_force_fpic.patch"),
            self.patch_file
        )
    
    def download(self):
        """
        Download ParMETIS and its dependencies
        """
        logging.info("Downloading GKlib, METIS, and ParMETIS")
        os.chdir(self.parmetis_dir)
        
        # Clone GKlib repository
        logging.info("Cloning GKlib")
        clone_repository(
            url="https://github.com/KarypisLab/GKlib.git",
            directory="gklib"
        )
        os.chdir(os.path.join(self.parmetis_dir, "gklib"))
        run_command(["git", "checkout", "8bd6bad750b2b0d908"])
        
        # Apply patch to GKlib
        apply_patch(self.patch_file, cwd=os.path.join(self.parmetis_dir, "gklib"))
        
        # Clone METIS repository
        logging.info("Cloning METIS")
        os.chdir(self.parmetis_dir)
        clone_repository(
            url="https://github.com/KarypisLab/METIS.git",
            directory="metis"
        )
        
        # Clone ParMETIS repository
        logging.info("Cloning ParMETIS")
        os.chdir(self.parmetis_dir)
        clone_repository(
            url="https://github.com/KarypisLab/ParMETIS.git",
            directory="parmetis"
        )
    
    def configure(self):
        """
        Configure is part of build for ParMETIS
        """
        pass
    
    def build(self):
        """
        Build ParMETIS and its dependencies
        """
        cc = self.env_vars.get("CC", "mpicc")
        
        # Build GKlib
        logging.info("Building GKlib")
        os.chdir(os.path.join(self.parmetis_dir, "gklib"))
        run_command([
            "make", 
            "config", 
            f"cc={cc}", 
            f"prefix={self.dep_install_dir}"
        ])
        run_command(["make", "install", f"-j{self.parallel_jobs}"])
        
        # Build METIS
        logging.info("Building METIS")
        os.chdir(os.path.join(self.parmetis_dir, "metis"))
        run_command([
            "make", 
            "config", 
            "shared=1", 
            f"cc={cc}", 
            f"prefix={self.dep_install_dir}",
            f"gklib_path={self.dep_install_dir}",
            "i64=1"
        ])
        run_command(["make", "install", f"-j{self.parallel_jobs}"])
        
        # Build ParMETIS
        logging.info("Building ParMETIS")
        os.chdir(os.path.join(self.parmetis_dir, "parmetis"))
        run_command([
            "make", 
            "config", 
            "shared=1", 
            f"cc={cc}", 
            f"prefix={self.dep_install_dir}",
            f"gklib_path={self.dep_install_dir}",
            f"metis_path={self.dep_install_dir}"
        ])
        run_command(["make", "install", f"-j{self.parallel_jobs}"])
    
    def install(self):
        """
        Installation is done as part of build
        """
        pass
    
    def cleanup(self):
        """
        Clean up build directory
        """
        logging.info("Cleaning up ParMETIS build directory")
        os.chdir(self.build_dir)
        if os.path.exists(self.parmetis_dir):
            shutil.rmtree(self.parmetis_dir)
        if os.path.exists(self.patch_file):
            os.remove(self.patch_file)