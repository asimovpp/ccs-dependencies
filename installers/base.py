#!/usr/bin/env python3
"""
Base installer class for CCS dependencies
"""
import os
import logging
import shutil
from utils.command import run_command


class BaseInstaller:
    """
    Base installer class for CCS dependencies
    """
    def __init__(self, config, env):
        """
        Initialize installer
        
        Args:
            config (dict): Configuration dictionary
            env (Environment): Environment object
        """
        self.config = config
        self.env = env
        self.env_vars = env.get_env_vars()
        self.install_dir = self.env_vars.get("INSTALL_DIR")
        self.build_dir = self.env_vars.get("BUILD_DIR")
        self.name = self.__class__.__name__.replace("Installer", "").lower()
        self.parallel_jobs = self.config.get("parallel_jobs", 16)
        
        # Set up dependency-specific variables
        self.version = self.env_vars.get(f"{self.name.upper()}_VERSION")
        self.dep_install_dir = self.env_vars.get(self.name.upper())
        
        if not self.version:
            logging.warning(f"Version not found for {self.name}")
            
        if not self.dep_install_dir:
            logging.warning(f"Install directory not found for {self.name}")
            compiler_type = self.env_vars.get("CMP", "unknown")
            if self.version:
                self.dep_install_dir = os.path.join(
                    self.install_dir, 
                    f"{self.name}-{compiler_type}-v{self.version}"
                )
            else:
                self.dep_install_dir = os.path.join(
                    self.install_dir, 
                    f"{self.name}-{compiler_type}"
                )
        
        # Set up source directory (where the source code will be downloaded)
        self.source_dir = os.path.join(self.build_dir, self.name)
        
        # Get dependency-specific configuration
        self.dep_config = self.config.get("dependencies", {}).get(self.name, {})
    
    def prepare(self):
        """
        Prepare build environment
        """
        logging.info(f"Preparing build environment for {self.name}")
        
        # Create build directory
        os.makedirs(self.build_dir, exist_ok=True)
        
        # Create install directory
        os.makedirs(self.dep_install_dir, exist_ok=True)
        
        # Change to build directory
        os.chdir(self.build_dir)
        
        # Remove existing source directory if it exists
        if os.path.exists(self.source_dir):
            logging.info(f"Removing existing source directory: {self.source_dir}")
            shutil.rmtree(self.source_dir)
    
    def download(self):
        """
        Download source code (to be implemented by subclasses)
        """
        raise NotImplementedError("Subclasses must implement download()")
    
    def configure(self):
        """
        Configure build (to be implemented by subclasses)
        """
        raise NotImplementedError("Subclasses must implement configure()")
    
    def build(self):
        """
        Build software (to be implemented by subclasses)
        """
        raise NotImplementedError("Subclasses must implement build()")
    
    def install(self):
        """
        Install software (to be implemented by subclasses)
        """
        raise NotImplementedError("Subclasses must implement install()")
    
    def cleanup(self):
        """
        Clean up build directory
        """
        logging.info(f"Cleaning up build directory for {self.name}")
        os.chdir(self.build_dir)
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
    
    def run(self):
        """
        Run the full installation process
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logging.info(f"Installing {self.name}")
            self.prepare()
            self.download()
            self.configure()
            self.build()
            self.install()
            self.cleanup()
            logging.info(f"Successfully installed {self.name}")
            return True
        except Exception as e:
            logging.error(f"Error installing {self.name}: {e}")
            return False