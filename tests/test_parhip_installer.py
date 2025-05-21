#!/usr/bin/env python3
"""
Test cases for ParHIP installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ccs_dep.installers.parhip import ParhipInstaller
from tests.test_installers_base import BaseInstallerTest


class TestParhipInstaller(BaseInstallerTest):
    """
    Test cases for ParHIP installer
    """
    
    def setup_parhip_config(self):
        """Set up ParHIP-specific configuration and environment variables"""
        # Set ParHIP version
        parhip_version = "3.14"
        
        # Update environment variables
        self.env_vars["PARHIP_VERSION"] = parhip_version
        self.env_vars["PARHIP"] = str(self.install_dir / f"parhip-gnu-v{parhip_version}")
        
        # Update configuration
        self.config["dependencies"]["parhip"] = {
            "version": parhip_version
        }
        
        return parhip_version
        
    def test_parhip_installer_prepare(self):
        """Test ParHIP installer prepare method"""
        # Setup
        self.setup_parhip_config()
        
        # Create installer
        installer = ParhipInstaller(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.name == "parhip"
        assert installer.version == "3.14"
    
    @patch("ccs_dep.installers.parhip.clone_repository")
    def test_parhip_installer_download(self, mock_clone):
        """Test ParHIP installer download method"""
        # Setup
        parhip_version = self.setup_parhip_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = ParhipInstaller(self.config, self.env)
        installer.prepare()
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly
        mock_clone.assert_called_once()
        args, kwargs = mock_clone.call_args
        assert kwargs["url"] == "https://github.com/KaHIP/KaHIP.git"
        assert kwargs["branch"] == f"v{parhip_version}"
        assert kwargs["depth"] == 1
    
    @patch("ccs_dep.installers.parhip.run_command")
    @patch("ccs_dep.installers.parhip.clone_repository")
    @patch("os.chdir")
    def test_parhip_installer_configure(self, mock_chdir, mock_clone, mock_run):
        """Test ParHIP installer configure method"""
        # Setup
        parhip_version = self.setup_parhip_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = ParhipInstaller(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        build_dir = source_dir / "build"
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading
        installer.download()
        
        # Test configure method
        installer.configure()
        
        # Verify configure command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert cmd[0] == "cmake"
        assert "-DCMAKE_BUILD_TYPE=Release" in cmd
        assert f"-DCMAKE_INSTALL_PREFIX={installer.dep_install_dir}" in cmd
        
        # Verify environment variables were set correctly
        env = kwargs.get("env", {})
        assert env["CC"] == self.env_vars["CC"]
    
    @patch("ccs_dep.installers.parhip.run_command")
    @patch("ccs_dep.installers.parhip.clone_repository")
    @patch("os.chdir")
    def test_parhip_installer_build(self, mock_chdir, mock_clone, mock_run):
        """Test ParHIP installer build method"""
        # Setup
        parhip_version = self.setup_parhip_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = ParhipInstaller(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        build_dir = source_dir / "build"
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading and configuring
        installer.download()
        installer.configure()
        mock_run.reset_mock()  # Reset after configure
        
        # Test build method
        installer.build()
        
        # Verify build command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert cmd[0] == "make"
        assert cmd[1] == "-j"
        assert cmd[2] == str(installer.parallel_jobs)
    
    @patch("ccs_dep.installers.parhip.run_command")
    @patch("ccs_dep.installers.parhip.clone_repository")
    @patch("os.chdir")
    def test_parhip_installer_install(self, mock_chdir, mock_clone, mock_run):
        """Test ParHIP installer install method"""
        # Setup
        parhip_version = self.setup_parhip_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = ParhipInstaller(self.config, self.env)
        
        # Override the source_dir before prepare to avoid removal
        installer.source_dir = str(Path(self.build_dir) / "parhip")
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        build_dir = source_dir / "build"
        build_dir.mkdir(parents=True, exist_ok=True)
        
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
        
        # Verify install command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert cmd[0] == "make"
        assert cmd[1] == "install"
    
    @patch("ccs_dep.installers.parhip.ParhipInstaller.prepare")
    @patch("ccs_dep.installers.parhip.ParhipInstaller.download")
    @patch("ccs_dep.installers.parhip.ParhipInstaller.configure")
    @patch("ccs_dep.installers.parhip.ParhipInstaller.build")
    @patch("ccs_dep.installers.parhip.ParhipInstaller.install")
    @patch("ccs_dep.installers.parhip.ParhipInstaller.cleanup")
    def test_parhip_installer_run(self, mock_cleanup, mock_install, mock_build, 
                               mock_configure, mock_download, mock_prepare):
        """Test ParHIP installer run method"""
        # Setup
        parhip_version = self.setup_parhip_config()
        
        # Create installer
        installer = ParhipInstaller(self.config, self.env)
        
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