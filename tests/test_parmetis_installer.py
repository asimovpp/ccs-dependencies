#!/usr/bin/env python3
"""
Test cases for ParMETIS installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from ccs_dep.installers.parmetis import ParmetisInstaller
from tests.test_installers_base import BaseInstallerTest


class TestParmetisInstaller(BaseInstallerTest):
    """
    Test cases for ParMETIS installer
    """
    
    def setup_parmetis_config(self):
        """Set up ParMETIS-specific configuration and environment variables"""
        # ParMETIS version
        parmetis_version = "4.0.3"
        
        # Update environment variables
        self.env_vars["PARMETIS_VERSION"] = parmetis_version
        self.env_vars["PARMETIS"] = str(self.install_dir / f"parmetis-gnu-v{parmetis_version}")
        
        # Update configuration
        self.config["dependencies"]["parmetis"] = {}
        
        return parmetis_version
    
    @patch("shutil.copy")
    def test_parmetis_installer_prepare(self, mock_copy):
        """Test ParMETIS installer prepare method"""
        # Setup
        parmetis_version = self.setup_parmetis_config()
        
        # Create mock patch directory and file
        patch_dir = self.temp_dir / "patch"
        patch_dir.mkdir(parents=True, exist_ok=True)
        patch_file = patch_dir / "gklib_force_fpic.patch"
        self.create_test_file(patch_file, "mock patch content")
        
        # Create installer with a custom _find_patch_file method
        installer = ParmetisInstaller(self.config, self.env)
        
        # Override the patch file location
        installer.patch_file = self.temp_dir / "build" / "gklib_force_fpic.patch"
        
        # Test prepare method
        with patch.object(installer, '_find_patch_file', return_value=patch_file):
            installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.name == "parmetis"
    
    @patch("ccs_dep.installers.parmetis.clone_repository")
    @patch("ccs_dep.installers.parmetis.apply_patch")
    @patch("ccs_dep.installers.parmetis.run_command")
    @patch("os.chdir")
    def test_parmetis_installer_download(self, mock_chdir, mock_run, mock_patch, mock_clone):
        """Test ParMETIS installer download method"""
        # Setup
        parmetis_version = self.setup_parmetis_config()
        mock_clone.return_value = True
        mock_patch.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = ParmetisInstaller(self.config, self.env)
        
        # Override paths for testing
        installer.parmetis_dir = self.temp_dir / "build" / "parmetis"
        installer.patch_file = self.temp_dir / "build" / "gklib_force_fpic.patch"
        
        # Create parmetis directory for testing
        installer.parmetis_dir.mkdir(parents=True, exist_ok=True)
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly for each repository
        assert mock_clone.call_count == 3
        
        # Verify patch was applied
        assert mock_patch.call_count == 1
        
        # Check clone calls for each repository
        urls = [call[1]["url"] for call in mock_clone.call_args_list]
        assert "GKlib" in urls[0]
        assert "METIS" in urls[1]
        assert "ParMETIS" in urls[2]
    
    @patch("ccs_dep.installers.parmetis.run_command")
    @patch("os.chdir")
    def test_parmetis_installer_build(self, mock_chdir, mock_run):
        """Test ParMETIS installer build method"""
        # Setup
        parmetis_version = self.setup_parmetis_config()
        mock_run.return_value = None
        
        # Create installer
        installer = ParmetisInstaller(self.config, self.env)
        
        # Setup paths for testing
        installer.parmetis_dir = self.temp_dir / "build" / "parmetis"
        installer.parmetis_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test directories
        (installer.parmetis_dir / "gklib").mkdir(parents=True, exist_ok=True)
        (installer.parmetis_dir / "metis").mkdir(parents=True, exist_ok=True)
        (installer.parmetis_dir / "parmetis").mkdir(parents=True, exist_ok=True)
        
        # Test build method
        installer.build()
        
        # Verify make commands were called for each component
        assert mock_run.call_count == 6  # 3 config + 3 install calls
        
        # Check configuration calls
        config_calls = [call for call in mock_run.call_args_list if "config" in call[0][0]]
        assert len(config_calls) == 3
        
        # Check install calls
        install_calls = [call for call in mock_run.call_args_list if "install" in call[0][0]]
        assert len(install_calls) == 3
    
    @patch("ccs_dep.installers.parmetis.ParmetisInstaller.prepare")
    @patch("ccs_dep.installers.parmetis.ParmetisInstaller.download")
    @patch("ccs_dep.installers.parmetis.ParmetisInstaller.build")
    @patch("ccs_dep.installers.parmetis.ParmetisInstaller.cleanup")
    def test_parmetis_installer_run(self, mock_cleanup, mock_build, mock_download, mock_prepare):
        """Test ParMETIS installer run method"""
        # Setup
        parmetis_version = self.setup_parmetis_config()
        
        # Create installer
        installer = ParmetisInstaller(self.config, self.env)
        
        # Add a _find_patch_file method for testing
        installer._find_patch_file = MagicMock(return_value=self.temp_dir / "patch" / "gklib_force_fpic.patch")
        
        # Test run method
        result = installer.run()
        
        # Verify result
        assert result is True
        
        # Verify all methods were called
        mock_prepare.assert_called_once()
        mock_download.assert_called_once()
        mock_build.assert_called_once()
        mock_cleanup.assert_called_once()
        
    def test_parmetis_installer_install(self):
        """Test ParMETIS installer install method"""
        # Setup
        parmetis_version = self.setup_parmetis_config()
        
        # Create installer
        installer = ParmetisInstaller(self.config, self.env)
        
        # Test install method (should be a pass-through since it's part of build)
        installer.install()
        
        # No assertions needed since this method is a no-op