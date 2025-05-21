#!/usr/bin/env python3
"""
Test cases for Makedepf90 installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ccs_dep.installers.makedepf90 import Makedepf90Installer
from tests.test_installers_base import BaseInstallerTest


class TestMakedepf90Installer(BaseInstallerTest):
    """
    Test cases for Makedepf90 installer
    """
    
    def setup_makedepf90_config(self):
        """Set up Makedepf90-specific configuration and environment variables"""
        # Update environment variables
        self.env_vars["MAKEDEPF90"] = str(self.install_dir / "makedepf90-gnu")
        
        # Update configuration
        self.config["dependencies"]["makedepf90"] = {}
        
    def test_makedepf90_installer_prepare(self):
        """Test Makedepf90 installer prepare method"""
        # Setup
        self.setup_makedepf90_config()
        
        # Create installer
        installer = Makedepf90Installer(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.name == "makedepf90"
    
    @patch("ccs_dep.installers.makedepf90.clone_repository")
    def test_makedepf90_installer_download(self, mock_clone):
        """Test Makedepf90 installer download method"""
        # Setup
        self.setup_makedepf90_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = Makedepf90Installer(self.config, self.env)
        installer.prepare()
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly
        mock_clone.assert_called_once()
        args, kwargs = mock_clone.call_args
        assert kwargs["url"] == "https://salsa.debian.org/science-team/makedepf90.git"
    
    @patch("ccs_dep.installers.makedepf90.run_command")
    @patch("ccs_dep.installers.makedepf90.clone_repository")
    @patch("os.chdir")
    def test_makedepf90_installer_configure(self, mock_chdir, mock_clone, mock_run):
        """Test Makedepf90 installer configure method"""
        # Setup
        self.setup_makedepf90_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Makedepf90Installer(self.config, self.env)
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
        assert cmd[0] == "./configure"
        assert f"--prefix={installer.dep_install_dir}" in cmd[1]
    
    @patch("ccs_dep.installers.makedepf90.run_command")
    @patch("ccs_dep.installers.makedepf90.clone_repository")
    @patch("os.chdir")
    def test_makedepf90_installer_build(self, mock_chdir, mock_clone, mock_run):
        """Test Makedepf90 installer build method"""
        # Setup
        self.setup_makedepf90_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Makedepf90Installer(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading and configuring
        installer.download()
        mock_run.reset_mock()  # Reset after configure
        
        # Test build method
        installer.build()
        
        # Verify build command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert cmd[0] == "make"
    
    @patch("ccs_dep.installers.makedepf90.run_command")
    @patch("ccs_dep.installers.makedepf90.clone_repository")
    @patch("os.chdir")
    @patch("shutil.copy2")
    @patch("pathlib.Path.exists")
    def test_makedepf90_installer_install(self, mock_exists, mock_copy2, mock_chdir, mock_clone, mock_run):
        """Test Makedepf90 installer install method"""
        # Setup
        self.setup_makedepf90_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        mock_exists.return_value = True
        
        # Create installer
        installer = Makedepf90Installer(self.config, self.env)
        
        # Override the source_dir before prepare to avoid removal
        installer.source_dir = str(Path(self.build_dir) / "makedepf90")
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Now call prepare but prevent rmtree from being called
        with patch("shutil.rmtree") as mock_rmtree:
            installer.prepare()
        
        # Mock downloading, configuring, and building
        installer.download()
        installer.configure()
        installer.build()
        mock_run.reset_mock()  # Reset after previous steps
        
        # Test install method
        installer.install()
        
        # Verify copy operation for binary
        mock_copy2.assert_called_once()
        args, kwargs = mock_copy2.call_args
        src, dest = args
        assert "makedepf90" in str(src)
        assert "bin" in str(dest)
    
    @patch("ccs_dep.installers.makedepf90.Makedepf90Installer.prepare")
    @patch("ccs_dep.installers.makedepf90.Makedepf90Installer.download")
    @patch("ccs_dep.installers.makedepf90.Makedepf90Installer.configure")
    @patch("ccs_dep.installers.makedepf90.Makedepf90Installer.build")
    @patch("ccs_dep.installers.makedepf90.Makedepf90Installer.install")
    @patch("ccs_dep.installers.makedepf90.Makedepf90Installer.cleanup")
    def test_makedepf90_installer_run(self, mock_cleanup, mock_install, mock_build, 
                                 mock_configure, mock_download, mock_prepare):
        """Test Makedepf90 installer run method"""
        # Setup
        self.setup_makedepf90_config()
        
        # Create installer
        installer = Makedepf90Installer(self.config, self.env)
        
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