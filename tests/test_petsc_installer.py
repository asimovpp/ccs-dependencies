#!/usr/bin/env python3
"""
Test cases for PETSc installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ccs_dep.installers.petsc import PetscInstaller
from tests.test_installers_base import BaseInstallerTest


class TestPetscInstaller(BaseInstallerTest):
    """
    Test cases for PETSc installer
    """
    
    def setup_petsc_config(self):
        """Set up PETSc-specific configuration and environment variables"""
        # PETSc version
        petsc_version = "3.21.2"
        
        # Update environment variables
        self.env_vars["PETSC_VERSION"] = petsc_version
        self.env_vars["PETSC"] = str(self.install_dir / f"petsc-gnu-v{petsc_version}")
        
        # Update configuration
        self.config["dependencies"]["petsc"] = {
            "configure_options": [
                "--download-fblaslapack=yes",
                "--with-fortran-datatypes=1",
                "--with-fortran-interfaces=1",
                "--with-fortran-bindings=1",
                "--with-fortran-kernels=1",
                "--with-debugging=1"
            ]
        }
        
        return petsc_version
    
    def test_petsc_installer_prepare(self):
        """Test PETSc installer prepare method"""
        # Setup
        petsc_version = self.setup_petsc_config()
        
        # Create installer
        installer = PetscInstaller(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.version == petsc_version
        assert installer.name == "petsc"
    
    @patch("ccs_dep.installers.petsc.clone_repository")
    @patch.dict("os.environ", {}, clear=True)
    def test_petsc_installer_download(self, mock_clone):
        """Test PETSc installer download method"""
        # Setup
        petsc_version = self.setup_petsc_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = PetscInstaller(self.config, self.env)
        installer.prepare()
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly
        mock_clone.assert_called_once()
        args, kwargs = mock_clone.call_args
        assert kwargs["url"] == "https://github.com/petsc/petsc.git"
        assert kwargs["branch"] == f"v{petsc_version}"
        assert kwargs["depth"] == 1
        
        # Verify PETSC_DIR environment variable was set
        assert "PETSC_DIR" in os.environ
        assert os.environ["PETSC_DIR"] == str(installer.source_dir)
    
    @patch("ccs_dep.installers.petsc.run_command")
    @patch("ccs_dep.installers.petsc.clone_repository")
    @patch("os.chdir")
    def test_petsc_installer_configure(self, mock_chdir, mock_clone, mock_run):
        """Test PETSc installer configure method"""
        # Setup
        petsc_version = self.setup_petsc_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = PetscInstaller(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading
        installer.download()
        
        # Test configure method
        installer.configure()
        
        # Verify configure command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert isinstance(cmd, list)
        assert cmd[0] == "./configure"
        assert f"--with-cc={self.env_vars['CC']}" in cmd
        assert f"--with-cxx={self.env_vars['CXX']}" in cmd
        assert f"--with-fc={self.env_vars['FC']}" in cmd
        assert f"--prefix={installer.dep_install_dir}" in cmd
        
        # Check that all configure options from config are included
        for option in self.config["dependencies"]["petsc"]["configure_options"]:
            assert option in cmd
    
    @patch("ccs_dep.installers.petsc.run_command")
    @patch("ccs_dep.installers.petsc.clone_repository")
    @patch("os.chdir")
    def test_petsc_installer_build(self, mock_chdir, mock_clone, mock_run):
        """Test PETSc installer build method"""
        # Setup
        petsc_version = self.setup_petsc_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = PetscInstaller(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading and configuring
        installer.download()
        mock_run.reset_mock()  # Reset after configure
        
        # Test build method
        installer.build()
        
        # Verify make command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert isinstance(cmd, list)
        assert cmd[0] == "make"
        assert any(arg.startswith("-j") for arg in cmd)
    
    @patch("ccs_dep.installers.petsc.run_command")
    @patch("ccs_dep.installers.petsc.clone_repository")
    @patch("os.chdir")
    def test_petsc_installer_install(self, mock_chdir, mock_clone, mock_run):
        """Test PETSc installer install method"""
        # Setup
        petsc_version = self.setup_petsc_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = PetscInstaller(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading, configuring, and building
        installer.download()
        mock_run.reset_mock()  # Reset after previous steps
        
        # Test install method
        installer.install()
        
        # Verify make install command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert isinstance(cmd, list)
        assert cmd[0] == "make"
        assert cmd[1] == "install"
    
    @patch("ccs_dep.installers.petsc.PetscInstaller.prepare")
    @patch("ccs_dep.installers.petsc.PetscInstaller.download")
    @patch("ccs_dep.installers.petsc.PetscInstaller.configure")
    @patch("ccs_dep.installers.petsc.PetscInstaller.build")
    @patch("ccs_dep.installers.petsc.PetscInstaller.install")
    @patch("ccs_dep.installers.petsc.PetscInstaller.cleanup")
    def test_petsc_installer_run(self, mock_cleanup, mock_install, mock_build, 
                               mock_configure, mock_download, mock_prepare):
        """Test PETSc installer run method"""
        # Setup
        petsc_version = self.setup_petsc_config()
        
        # Create installer
        installer = PetscInstaller(self.config, self.env)
        
        # Test run method
        result = installer.run()
        
        # Verify result
        assert result is True
        
        # Verify all methods were called
        mock_prepare.assert_called_once()
        mock_download.assert_called_once()
        mock_configure.assert_called_once()
        mock_build.assert_called_once()
        mock_install.assert_called_once()
        mock_cleanup.assert_called_once()