#!/usr/bin/env python3
"""
ParMETIS installer for CCS dependencies
"""
import os
import logging
import shutil
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command, clone_repository, apply_patch


class ParmetisInstaller(BaseInstaller):
    """
    ParMETIS installer
    """

    def __init__(self, config, env):
        super().__init__(config, env)
        self.patch_file = None
        self.parmetis_dir = None

    def _find_patch_file(self):
        """
        Find the path to the patch file
        
        Returns:
            Path: Path to the patch file
        """
        module_path = Path(__file__).parent.parent
        patch_dir = module_path.parent / "patch"
        return patch_dir / "gklib_force_fpic.patch"
    
    def prepare(self):
        """
        Prepare build environment
        """
        super().prepare()
        
        # Create a subdirectory for ParMETIS and its dependencies
        build_dir = Path(self.build_dir)
        self.parmetis_dir = build_dir / "parmetis"
        self.parmetis_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy patch file if needed
        self.patch_file = build_dir / "gklib_force_fpic.patch"
        patch_source = self._find_patch_file()
        shutil.copy(
            patch_source,
            self.patch_file
        )
    
    def download(self):
        """
        Download ParMETIS and its dependencies
        """
        logging.info("Downloading GKlib, METIS, and ParMETIS")
        os.chdir(str(self.parmetis_dir))
        
        # Clone GKlib repository
        logging.info("Cloning GKlib")
        gklib_dir = self.parmetis_dir / "gklib"
        clone_repository(
            url="https://github.com/KarypisLab/GKlib.git",
            directory=gklib_dir
        )
        os.chdir(gklib_dir)
        run_command(["git", "checkout", "8bd6bad750b2b0d908"])
        
        # Apply patch to GKlib
        apply_patch(self.patch_file, cwd=str(gklib_dir))
        
        # Clone METIS repository
        logging.info("Cloning METIS")
        os.chdir(self.parmetis_dir)
        metis_dir = self.parmetis_dir / "metis"
        clone_repository(
            url="https://github.com/KarypisLab/METIS.git",
            directory=metis_dir
        )
        
        # Clone ParMETIS repository
        logging.info("Cloning ParMETIS")
        os.chdir(self.parmetis_dir)
        parmetis_dir = self.parmetis_dir / "parmetis"
        clone_repository(
            url="https://github.com/KarypisLab/ParMETIS.git",
            directory=parmetis_dir
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
        install_dir = Path(self.dep_install_dir)
        
        # Build GKlib
        logging.info("Building GKlib")
        gklib_dir = self.parmetis_dir / "gklib"
        os.chdir(str(gklib_dir))
        run_command([
            "make", 
            "config", 
            f"cc={cc}", 
            f"prefix={install_dir}"
        ])
        run_command(["make", "install", f"-j{self.parallel_jobs}"])
        
        # Build METIS
        logging.info("Building METIS")
        metis_dir = self.parmetis_dir / "metis"
        os.chdir(metis_dir)
        run_command([
            "make", 
            "config", 
            "shared=1", 
            f"cc={cc}", 
            f"prefix={install_dir}",
            f"gklib_path={install_dir}",
            "i64=1"
        ])
        run_command(["make", "install", f"-j{self.parallel_jobs}"])
        
        # Build ParMETIS
        logging.info("Building ParMETIS")
        parmetis_dir = self.parmetis_dir / "parmetis"
        os.chdir(parmetis_dir)
        run_command([
            "make", 
            "config", 
            "shared=1", 
            f"cc={cc}", 
            f"prefix={install_dir}",
            f"gklib_path={install_dir}",
            f"metis_path={install_dir}"
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
        build_dir = Path(self.build_dir)
        os.chdir(build_dir)
        
        if self.parmetis_dir.exists():
            shutil.rmtree(self.parmetis_dir)
        
        patch_file = Path(self.patch_file)
        if patch_file.exists():
            patch_file.unlink()