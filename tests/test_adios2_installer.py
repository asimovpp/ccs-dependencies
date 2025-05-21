#!/usr/bin/env python3
"""
Test cases for ADIOS2 installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ccs_dep.installers.adios2 import Adios2Installer
from tests.test_installers_base import BaseInstallerTest


class TestAdios2Installer(BaseInstallerTest):
    """
    Test cases for ADIOS2 installer
    """
    
    def setup_adios2_config(self):
        """Set up ADIOS2-specific configuration and environment variables"""
        # Set ADIOS2 version
        adios2_version = "2.10.1"
        
        # Update environment variables
        self.env_vars["ADIOS2_VERSION"] = adios2_version
        self.env_vars["ADIOS2"] = str(self.install_dir / f"adios2-gnu-v{adios2_version}")
        self.env_vars["HDF5_ROOT"] = str(self.install_dir / "hdf5-gnu-v1.14.4.3")
        
        # Update configuration
        self.config["dependencies"]["adios2"] = {
            "version": adios2_version
        }
        
        return adios2_version
        
    def test_adios2_installer_prepare(self):
        """Test ADIOS2 installer prepare method"""
        # Setup
        self.setup_adios2_config()
        
        # Create installer
        installer = Adios2Installer(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.name == "adios2"
        assert installer.version == "2.10.1"
    
    @patch("ccs_dep.installers.adios2.clone_repository")
    def test_adios2_installer_download(self, mock_clone):
        """Test ADIOS2 installer download method"""
        # Setup
        adios2_version = self.setup_adios2_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = Adios2Installer(self.config, self.env)
        installer.prepare()
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly
        mock_clone.assert_called_once()
        args, kwargs = mock_clone.call_args
        assert kwargs["url"] == "https://github.com/ornladios/ADIOS2.git"
        assert kwargs["branch"] == f"v{adios2_version}"
        assert kwargs["depth"] == 1
    
    @patch("ccs_dep.installers.adios2.run_command")
    @patch("ccs_dep.installers.adios2.clone_repository")
    @patch("os.chdir")
    def test_adios2_installer_configure(self, mock_chdir, mock_clone, mock_run):
        """Test ADIOS2 installer configure method"""
        # Setup
        adios2_version = self.setup_adios2_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Adios2Installer(self.config, self.env)
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
        assert "-DADIOS2_USE_Fortran=ON" in cmd
        assert "-DADIOS2_USE_MPI=ON" in cmd
        assert "-DADIOS2_USE_HDF5=ON" in cmd
        assert f"-DHDF5_ROOT={self.env_vars['HDF5_ROOT']}" in cmd
        assert f"-DCMAKE_INSTALL_PREFIX={installer.dep_install_dir}" in cmd
    
    @patch("ccs_dep.installers.adios2.run_command")
    @patch("ccs_dep.installers.adios2.clone_repository")
    @patch("os.chdir")
    def test_adios2_installer_build(self, mock_chdir, mock_clone, mock_run):
        """Test ADIOS2 installer build method"""
        # Setup
        adios2_version = self.setup_adios2_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Adios2Installer(self.config, self.env)
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
    
    @patch("ccs_dep.installers.adios2.run_command")
    @patch("ccs_dep.installers.adios2.clone_repository")
    @patch("os.chdir")
    def test_adios2_installer_install(self, mock_chdir, mock_clone, mock_run):
        """Test ADIOS2 installer install method"""
        # Setup
        adios2_version = self.setup_adios2_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = Adios2Installer(self.config, self.env)
        
        # Override the source_dir before prepare to avoid removal
        installer.source_dir = str(Path(self.build_dir) / "adios2")
        
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
    
    @patch("ccs_dep.installers.adios2.Adios2Installer.prepare")
    @patch("ccs_dep.installers.adios2.Adios2Installer.download")
    @patch("ccs_dep.installers.adios2.Adios2Installer.configure")
    @patch("ccs_dep.installers.adios2.Adios2Installer.build")
    @patch("ccs_dep.installers.adios2.Adios2Installer.install")
    @patch("ccs_dep.installers.adios2.Adios2Installer.cleanup")
    def test_adios2_installer_run(self, mock_cleanup, mock_install, mock_build, 
                                mock_configure, mock_download, mock_prepare):
        """Test ADIOS2 installer run method"""
        # Setup
        adios2_version = self.setup_adios2_config()
        
        # Create installer
        installer = Adios2Installer(self.config, self.env)
        
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