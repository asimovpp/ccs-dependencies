#!/usr/bin/env python3
"""
Test cases for RCM-f90 installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ccs_dep.installers.rcm_f90 import RcmF90Installer
from tests.test_installers_base import BaseInstallerTest


class TestRcmF90Installer(BaseInstallerTest):
    """
    Test cases for RCM-f90 installer
    """
    
    def setup_rcm_f90_config(self):
        """Set up RCM-f90-specific configuration and environment variables"""
        # Set RCM-f90 version
        rcm_f90_version = "1.0.0"
        
        # Update environment variables
        self.env_vars["RCM_F90_VERSION"] = rcm_f90_version
        self.env_vars["RCMF90_VERSION"] = rcm_f90_version  # For BaseInstaller
        self.env_vars["RCMF90"] = str(self.install_dir / f"rcm-f90-gnu-v{rcm_f90_version}")
        
        # Update configuration
        self.config["dependencies"]["rcm_f90"] = {
            "version": rcm_f90_version
        }
        
    def test_rcm_f90_installer_prepare(self):
        """Test RCM-f90 installer prepare method"""
        # Setup
        self.setup_rcm_f90_config()
        
        # Create installer
        installer = RcmF90Installer(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.name == "rcm_f90"
    
    @patch("ccs_dep.installers.rcm_f90.clone_repository")
    def test_rcm_f90_installer_download(self, mock_clone):
        """Test RCM-f90 installer download method"""
        # Setup
        self.setup_rcm_f90_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = RcmF90Installer(self.config, self.env)
        installer.prepare()
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly
        mock_clone.assert_called_once()
        args, kwargs = mock_clone.call_args
        assert kwargs["url"] == "https://github.com/asimovpp/RCM-f90.git"
        assert kwargs["depth"] == 1
    
    @patch("ccs_dep.installers.rcm_f90.run_command")
    @patch("ccs_dep.installers.rcm_f90.clone_repository")
    @patch("os.chdir")
    def test_rcm_f90_installer_build(self, mock_chdir, mock_clone, mock_run):
        """Test RCM-f90 installer build method"""
        # Setup
        self.setup_rcm_f90_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Set compiler type in environment
        self.env_vars["CMP"] = "gnu_ubuntu"
        
        # Create installer
        installer = RcmF90Installer(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading
        installer.download()
        
        # Test build method
        installer.build()
        
        # Verify make command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert isinstance(cmd, list)
        assert cmd[0] == "make"
        assert cmd[1] == "CMP=gnu"  # Should extract gnu from gnu_ubuntu
    
    @patch("ccs_dep.installers.rcm_f90.clone_repository")
    @patch("os.chdir")
    @patch("shutil.copytree")
    def test_rcm_f90_installer_install(self, mock_copytree, mock_chdir, mock_clone):
        """Test RCM-f90 installer install method"""
        # Setup
        self.setup_rcm_f90_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = RcmF90Installer(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory structure for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        lib_dir = source_dir / "lib"
        include_dir = source_dir / "include"
        lib_dir.mkdir(parents=True, exist_ok=True)
        include_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a test file in each directory
        (lib_dir / "test.a").touch()
        (include_dir / "test.h").touch()
        
        # Mock downloading
        installer.download()
        
        # Test install method
        installer.install()
        
        # Verify copytree was called correctly for both directories
        assert mock_copytree.call_count == 2
        
        # Extract destination paths from calls
        call_args_list = mock_copytree.call_args_list
        dest_dirs = [call[0][1] for call in call_args_list]
        
        # Verify destination paths
        assert Path(installer.dep_install_dir) / "lib" in dest_dirs
        assert Path(installer.dep_install_dir) / "include" in dest_dirs
    
    @patch("ccs_dep.installers.rcm_f90.RcmF90Installer.prepare")
    @patch("ccs_dep.installers.rcm_f90.RcmF90Installer.download")
    @patch("ccs_dep.installers.rcm_f90.RcmF90Installer.build")
    @patch("ccs_dep.installers.rcm_f90.RcmF90Installer.install")
    @patch("ccs_dep.installers.rcm_f90.RcmF90Installer.cleanup")
    def test_rcm_f90_installer_run(self, mock_cleanup, mock_install, mock_build, 
                                  mock_download, mock_prepare):
        """Test RCM-f90 installer run method"""
        # Setup
        self.setup_rcm_f90_config()
        
        # Create installer
        installer = RcmF90Installer(self.config, self.env)
        
        # Test run method
        result = installer.run()
        
        # Verify result
        assert result is True
        
        # Verify all methods were called
        mock_prepare.assert_called_once()
        mock_download.assert_called_once()
        mock_build.assert_called_once()
        mock_install.assert_called_once()
        mock_cleanup.assert_called_once()