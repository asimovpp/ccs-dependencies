#!/usr/bin/env python3
"""
Test cases for HDF5 installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ccs_dep.installers.hdf5 import Hdf5Installer
from tests.test_installers_base import BaseInstallerTest


class TestHdf5Installer(BaseInstallerTest):
    """
    Test cases for HDF5 installer
    """
    
    def setup_hdf5_config(self):
        """Set up HDF5-specific configuration and environment variables"""
        # HDF5 version
        hdf5_version = "1.14.4.3"
        
        # Update environment variables
        self.env_vars["HDF5_VERSION"] = hdf5_version
        self.env_vars["HDF5"] = str(self.install_dir / f"hdf5-gnu-v{hdf5_version}")
        
        # Update configuration
        self.config["dependencies"]["hdf5"] = {
            "configure_options": ["--enable-parallel"]
        }
        
        return hdf5_version
    
    def test_hdf5_installer_prepare(self):
        """Test HDF5 installer prepare method"""
        # Setup
        hdf5_version = self.setup_hdf5_config()
        
        # Create installer
        installer = Hdf5Installer(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.version == hdf5_version
        assert installer.name == "hdf5"
    
    @patch("ccs_dep.installers.hdf5.clone_repository")
    def test_hdf5_installer_download(self, mock_clone):
        """Test HDF5 installer download method"""
        # Setup
        hdf5_version = self.setup_hdf5_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = Hdf5Installer(self.config, self.env)
        installer.prepare()
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly
        mock_clone.assert_called_once()
        args, kwargs = mock_clone.call_args
        assert kwargs["url"] == "https://github.com/HDFGroup/hdf5.git"
        assert kwargs["branch"] == f"hdf5_{hdf5_version}"
        assert kwargs["depth"] == 1
    
    @patch("ccs_dep.installers.hdf5.run_command")
    @patch("ccs_dep.installers.hdf5.clone_repository")
    def test_hdf5_installer_configure(self, mock_clone, mock_run):
        """Test HDF5 installer configure method"""
        # Setup
        self.setup_hdf5_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Hdf5Installer(self.config, self.env)
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
        assert "--enable-parallel" in cmd
        assert any(arg.startswith("--prefix=") for arg in cmd)
    
    @patch("ccs_dep.installers.hdf5.run_command")
    @patch("ccs_dep.installers.hdf5.clone_repository")
    @patch("os.chdir")
    def test_hdf5_installer_build(self, mock_chdir, mock_clone, mock_run):
        """Test HDF5 installer build method"""
        # Setup
        self.setup_hdf5_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Hdf5Installer(self.config, self.env)
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
    
    @patch("ccs_dep.installers.hdf5.run_command")
    @patch("ccs_dep.installers.hdf5.clone_repository")
    @patch("os.chdir")
    def test_hdf5_installer_install(self, mock_chdir, mock_clone, mock_run):
        """Test HDF5 installer install method"""
        # Setup
        self.setup_hdf5_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Hdf5Installer(self.config, self.env)
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
    
    @patch("ccs_dep.installers.hdf5.Hdf5Installer.prepare")
    @patch("ccs_dep.installers.hdf5.Hdf5Installer.download")
    @patch("ccs_dep.installers.hdf5.Hdf5Installer.configure")
    @patch("ccs_dep.installers.hdf5.Hdf5Installer.build")
    @patch("ccs_dep.installers.hdf5.Hdf5Installer.install")
    @patch("ccs_dep.installers.hdf5.Hdf5Installer.cleanup")
    def test_hdf5_installer_run(self, mock_cleanup, mock_install, mock_build, 
                               mock_configure, mock_download, mock_prepare):
        """Test HDF5 installer run method"""
        # Setup
        self.setup_hdf5_config()
        
        # Create installer
        installer = Hdf5Installer(self.config, self.env)
        
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