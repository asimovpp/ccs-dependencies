#!/usr/bin/env python3
"""
FYAML-C installer for CCS dependencies
"""
import os
import logging
import shutil
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command, clone_repository


class FyamlCInstaller(BaseInstaller):
    """
    FYAML-C installer

    FYAML-C is a Fortran YAML parser that uses the C library libyaml.
    """
    
    def __init__(self, config, env):
        """
        Initialize the FYAML-C installer
        
        Args:
            config (dict): Configuration dictionary
            env (Environment): Environment object
        """
        super().__init__(config, env)
        # Override the name determined from the class name to match the expected format
        self.name = "fyaml_c"
        
        # Check if we need to update the version
        if not self.version and "FYAML_C_VERSION" in self.env_vars:
            self.version = self.env_vars.get("FYAML_C_VERSION")
            
        # Check if we need to update the installation directory
        if "FYAML_C" in self.env_vars:
            self.dep_install_dir = self.env_vars.get("FYAML_C")

    def download(self):
        """
        Download FYAML-C source code
        """
        logging.info(f"Downloading FYAML-C version {self.version}")
        os.chdir(self.build_dir)
        
        # Clone FYAML-C repository
        source_dir = Path(self.source_dir)
        clone_repository(
            url="https://github.com/Nicholaswogan/fortran-yaml-c.git",
            directory=source_dir,
            branch=f"v{self.version}",
            depth=1
        )
    
    def configure(self):
        """
        Configure FYAML-C build
        """
        logging.info("Configuring FYAML-C")
        source_dir = Path(self.source_dir)
        
        # Create build directory
        build_dir = source_dir / "build"
        build_dir.mkdir(exist_ok=True)
        os.chdir(build_dir)
        
        # Clear environment variables that might interfere with the build
        env_vars = os.environ.copy()
        for var in ["HDF5_ROOT", "HDF5_DIR", "PETSC_ROOT", "PETSC_DIR"]:
            if var in env_vars:
                del env_vars[var]
        
        # Run CMake configuration
        run_command([
            "cmake", 
            f"-DCMAKE_INSTALL_PREFIX={self.dep_install_dir}",
            "-DBUILD_SHARED_LIBS=ON",
            "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
            ".."
        ], env=env_vars)
    
    def build(self):
        """
        Build FYAML-C
        """
        logging.info("Building FYAML-C")
        source_dir = Path(self.source_dir)
        build_dir = source_dir / "build"
        os.chdir(build_dir)
        
        # Run CMake build
        run_command(["cmake", "--build", "."])
    
    def install(self):
        """
        Install FYAML-C
        """
        logging.info("Installing FYAML-C")
        source_dir = Path(self.source_dir)
        build_dir = source_dir / "build"
        
        # Create installation directories
        install_dir = Path(self.dep_install_dir)
        lib_dir = install_dir / "lib"
        modules_dir = install_dir / "modules"
        
        lib_dir.mkdir(parents=True, exist_ok=True)
        modules_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy modules directory
        modules_src = build_dir / "modules"
        if modules_src.exists():
            # Copy contents of modules directory
            shutil.copytree(modules_src, modules_dir, dirs_exist_ok=True)
        else:
            logging.error(f"Unable to copy module source files to {modules_dir}")
        
        # Copy shared libraries
        lib_src = build_dir / "src"
        for so_file in list(lib_src.glob("*.so")) + list(lib_src.glob("*.dylib")):
            shutil.copy2(so_file, lib_dir)
        
        # Copy libyaml.so from dependencies
        libyaml_so = build_dir / "_deps" / "libyaml-build" / "libyaml.so"
        if libyaml_so.exists():
            shutil.copy2(libyaml_so, lib_dir)
        else:
            logging.warning(f"Could not find {libyaml_so}")
            # Try alternative paths
            alt_paths = [
                build_dir / "_deps" / "libyaml-build" / "libyaml.dylib",
                build_dir / "_deps" / "libyaml-build" / "src" / "libyaml.so",
                build_dir / "_deps" / "libyaml-build" / "src" / "libyaml.dylib",
                build_dir / "_deps" / "libyaml-build" / "lib" / "libyaml.so",
                build_dir / "_deps" / "libyaml-build" / "lib" / "libyaml.dylib",
            ]
            for alt_path in alt_paths:
                if alt_path.exists():
                    logging.info(f"Found libyaml.so at {alt_path}")
                    shutil.copy2(alt_path, lib_dir)
                    break
            else:
                logging.warning("Could not find libyaml.so in any expected location")
                logging.info("Attempting to use CMake install as fallback")
                os.chdir(build_dir)
                run_command(["cmake", "--install", "."])