#!/usr/bin/env python3
"""
Environment setup utilities for CCS dependencies
"""
import os
import logging
import platform
import tempfile
from pathlib import Path


class Environment:
    """
    Environment setup for CCS dependencies
    """
    def __init__(self, env_name, config):
        """
        Initialize environment
        
        Args:
            env_name (str): Environment name (e.g., gnu_ubuntu, gnu_macos)
            config (dict): Configuration dictionary
        """
        self.env_name = env_name
        self.config = config
        self.env_vars = {}
        self.setup_environment()
        
    def setup_environment(self):
        """Set up environment variables based on config"""
        # Set up compiler variables
        self.env_vars["CC"] = str(self.config.get("cc", "mpicc"))
        self.env_vars["CXX"] = str(self.config.get("cxx", "mpicxx"))
        self.env_vars["FC"] = str(self.config.get("fc", "mpifort"))
        
        # Set up basic environment variables
        install_dir = self.config.get("install_dir", "~/ccs-deps")
        
        # Get temporary directory in a cross-platform way
        tmp_dir = Path(tempfile.gettempdir())
        default_build_dir = tmp_dir / "build-ccs-deps"
        build_dir = self.config.get("build_dir", str(default_build_dir))
        
        # Extract compiler type
        compiler_type = self.env_name.split("_")[0]  # e.g., gnu, cray
        
        # Expand ~ in paths and convert to Path objects
        install_dir = Path(install_dir).expanduser()
        build_dir = Path(build_dir).expanduser()
        
        self.env_vars["INSTALL_DIR"] = str(install_dir)
        self.env_vars["BUILD_DIR"] = str(build_dir)
        self.env_vars["CMP"] = compiler_type
        
        # Set up dependency-specific variables
        deps_config = self.config.get("dependencies", {})
        for dep_name, dep_config in deps_config.items():
            if "version" in dep_config:
                version = str(dep_config["version"])
                self.env_vars[f"{dep_name.upper()}_VERSION"] = version
                
                # Set specific install paths for each dependency
                dep_install_dir = install_dir / f"{dep_name}-{compiler_type}-v{version}"
                self.env_vars[dep_name.upper()] = str(dep_install_dir)
                
                # Special case for HDF5
                if dep_name == "hdf5":
                    self.env_vars["HDF5_ROOT"] = str(dep_install_dir)
        
        # Add Python path
        python_path = install_dir / f"python-{compiler_type}"
        self.env_vars["PYTHONPATH"] = f"{python_path}:{os.environ.get('PYTHONPATH', '')}"
        self.env_vars["PATH"] = f"{python_path}/bin:{os.environ.get('PATH', '')}"
        self.env_vars["PYTHONUSERBASE"] = str(python_path)
        
        # Set library paths for dependencies
        ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
        for dep_var in ["PETSC", "FYAMLC", "PARHIP", "PARMETIS", "RCMF90"]:
            if dep_var in self.env_vars:
                lib_path = Path(self.env_vars[dep_var]) / "lib"
                ld_library_path = f"{lib_path}:{ld_library_path}"
        
        self.env_vars["LD_LIBRARY_PATH"] = ld_library_path
        
        # Add binary paths to PATH
        for dep_var in ["MAKEDEPF90"]:
            if dep_var in self.env_vars:
                bin_path = Path(self.env_vars[dep_var]) / "bin"
                self.env_vars["PATH"] = f"{bin_path}:{self.env_vars['PATH']}"
                
    def get_env_vars(self):
        """Get environment variables as a dictionary"""
        return self.env_vars
        
    def get_install_dir(self):
        """Get installation directory"""
        return self.env_vars["INSTALL_DIR"]
        
    def get_build_dir(self):
        """Get build directory"""
        return self.env_vars["BUILD_DIR"]
        
    def apply(self):
        """Apply environment variables to the current process"""
        for key, value in self.env_vars.items():
            os.environ[key] = str(value)  # Ensure all values are strings
            logging.debug(f"Set environment variable: {key}={value}")
        
    def print_environment(self):
        """Print environment variables"""
        logging.info(f"Environment: {self.env_name}")
        logging.info(f"Compiler: {self.env_vars.get('CMP', 'unknown')}")
        logging.info(f"Build directory: {self.env_vars.get('BUILD_DIR', 'unknown')}")
        logging.info(f"Install directory: {self.env_vars.get('INSTALL_DIR', 'unknown')}")