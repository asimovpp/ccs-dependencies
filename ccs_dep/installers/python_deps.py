#!/usr/bin/env python3
"""
Python dependencies installer for CCS dependencies (PyYAML, LIT, etc.)
"""
import os
import sys
import logging
import shutil
import venv
import subprocess
from pathlib import Path
from ccs_dep.installers.base import BaseInstaller
from ccs_dep.utils.command import run_command


class PythonDepsInstaller(BaseInstaller):
    """
    Python dependencies installer

    Installs Python dependencies required for CCS (PyYAML, LIT, etc.)
    using a virtual environment for isolation.
    """
    
    def __init__(self, config, env):
        """
        Initialize the Python dependencies installer
        
        Args:
            config (dict): Configuration dictionary
            env (Environment): Environment object
        """
        super().__init__(config, env)
        
        # Override the name determined from the class name
        self.name = "python_deps"
        
        # Check if we need to update the installation directory
        if not self.dep_install_dir and "PYTHON_DEPS" in self.env_vars:
            self.dep_install_dir = self.env_vars.get("PYTHON_DEPS")
            
        # Get the list of dependencies to install
        self.dependencies = self.dep_config.get("packages", ["pyyaml", "lit", "flinter", "fprettify"])
        
    def download(self):
        """
        No download needed for Python dependencies
        """
        logging.info("No download required for Python dependencies")
        pass
    
    def configure(self):
        """
        Create and configure a Python virtual environment
        """
        logging.info("Creating Python virtual environment")
        venv_dir = Path(self.dep_install_dir)
        
        # Create the virtual environment
        venv.create(venv_dir, with_pip=True)
    
    def build(self):
        """
        No build step needed for Python dependencies
        """
        logging.info("No build required for Python dependencies")
        pass
    
    def install(self):
        """
        Install Python dependencies into the virtual environment
        """
        logging.info(f"Installing Python dependencies: {', '.join(self.dependencies)}")
        venv_dir = Path(self.dep_install_dir)
        
        # Determine the pip executable path based on the platform
        if sys.platform == "win32":
            pip_path = venv_dir / "Scripts" / "pip"
        else:
            pip_path = venv_dir / "bin" / "pip"
        
        # Upgrade pip first
        run_command([str(pip_path), "install", "--upgrade", "pip"])
        
        # Install each dependency
        for package in self.dependencies:
            logging.info(f"Installing {package}")
            run_command([str(pip_path), "install", package])
            
        # Create activation scripts that add the virtual environment to PATH
        self._create_activation_scripts(venv_dir)
    
    def _create_activation_scripts(self, venv_dir):
        """
        Create activation scripts for different shells
        
        Args:
            venv_dir (Path): Path to the virtual environment directory
        """
        # Create a bash activation script
        bash_script = venv_dir / "activate.sh"
        with open(bash_script, "w") as f:
            f.write(f"""#!/bin/bash
# Add Python venv bin directory to PATH
export PATH="{venv_dir}/bin:$PATH"
""")
        
        # Create a csh activation script
        csh_script = venv_dir / "activate.csh"
        with open(csh_script, "w") as f:
            f.write(f"""#!/bin/csh
# Add Python venv bin directory to PATH
setenv PATH "{venv_dir}/bin:$PATH"
""")
        
        # Make the scripts executable
        os.chmod(bash_script, 0o755)
        os.chmod(csh_script, 0o755)
        
        logging.info(f"Created activation scripts: {bash_script}, {csh_script}")
        
    def cleanup(self):
        """
        No cleanup needed for Python dependencies
        """
        logging.info("No cleanup required for Python dependencies")
        # Skip the default cleanup to preserve the virtual environment
        pass