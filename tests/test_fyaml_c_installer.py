#!/usr/bin/env python3
"""
Test cases for FYAML-C installer
"""
import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from ccs_dep.installers.fyaml_c import FyamlCInstaller
from tests.test_installers_base import BaseInstallerTest


class TestFyamlCInstaller(BaseInstallerTest):
    """
    Test cases for FYAML-C installer
    """
    
    def setup_fyaml_c_config(self):
        """Set up FYAML-C-specific configuration and environment variables"""
        # Set FYAML-C version
        fyaml_c_version = "0.2.6"
        
        # Update environment variables
        self.env_vars["FYAMLC_VERSION"] = fyaml_c_version
        self.env_vars["FYAMLC"] = str(self.install_dir / f"fyaml-c-gnu-v{fyaml_c_version}")
        
        # Set environment variables that should be cleared during build
        self.env_vars["HDF5_ROOT"] = "/path/to/hdf5"
        self.env_vars["HDF5_DIR"] = "/path/to/hdf5"
        self.env_vars["PETSC_ROOT"] = "/path/to/petsc"
        self.env_vars["PETSC_DIR"] = "/path/to/petsc"
        
        # Update configuration
        self.config["dependencies"]["fyaml_c"] = {
            "version": fyaml_c_version
        }
        
        return fyaml_c_version
        
    def test_fyaml_c_installer_prepare(self):
        """Test FYAML-C installer prepare method"""
        # Setup
        self.setup_fyaml_c_config()
        
        # Create installer
        installer = FyamlCInstaller(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.name == "fyaml_c"
        assert installer.version == "0.2.6"
    
    @patch("ccs_dep.installers.fyaml_c.clone_repository")
    def test_fyaml_c_installer_download(self, mock_clone):
        """Test FYAML-C installer download method"""
        # Setup
        fyaml_c_version = self.setup_fyaml_c_config()
        mock_clone.return_value = True
        
        # Create installer
        installer = FyamlCInstaller(self.config, self.env)
        installer.prepare()
        
        # Test download method
        installer.download()
        
        # Verify clone was called correctly
        mock_clone.assert_called_once()
        args, kwargs = mock_clone.call_args
        assert kwargs["url"] == "https://github.com/Nicholaswogan/fortran-yaml-c.git"
        assert kwargs["branch"] == f"v{fyaml_c_version}"
        assert kwargs["depth"] == 1
    
    @patch("ccs_dep.installers.fyaml_c.run_command")
    @patch("ccs_dep.installers.fyaml_c.clone_repository")
    @patch("os.chdir")
    def test_fyaml_c_installer_configure(self, mock_chdir, mock_clone, mock_run):
        """Test FYAML-C installer configure method"""
        # Setup
        fyaml_c_version = self.setup_fyaml_c_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = FyamlCInstaller(self.config, self.env)
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
        assert isinstance(cmd, list)
        assert cmd[0] == "cmake"
        assert f"-DCMAKE_INSTALL_PREFIX={installer.dep_install_dir}" in cmd[1]
        assert "-DBUILD_SHARED_LIBS=ON" in cmd
        
        # Verify environment variables were cleared
        env = kwargs.get("env", {})
        assert "HDF5_ROOT" not in env
        assert "HDF5_DIR" not in env
        assert "PETSC_ROOT" not in env
        assert "PETSC_DIR" not in env
    
    @patch("ccs_dep.installers.fyaml_c.run_command")
    @patch("ccs_dep.installers.fyaml_c.clone_repository")
    @patch("os.chdir")
    def test_fyaml_c_installer_build(self, mock_chdir, mock_clone, mock_run):
        """Test FYAML-C installer build method"""
        # Setup
        fyaml_c_version = self.setup_fyaml_c_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Create installer
        installer = FyamlCInstaller(self.config, self.env)
        installer.prepare()
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        build_dir = source_dir / "build"
        build_dir.mkdir(parents=True, exist_ok=True)
        
        # Mock downloading and configuring
        installer.download()
        mock_run.reset_mock()  # Reset after configure
        
        # Test build method
        installer.build()
        
        # Verify build command was called correctly
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert isinstance(cmd, list)
        assert cmd[0] == "cmake"
        assert cmd[1] == "--build"
        assert cmd[2] == "."
    
    @patch("ccs_dep.installers.fyaml_c.run_command")
    @patch("ccs_dep.installers.fyaml_c.clone_repository")
    @patch("os.chdir")
    @patch("shutil.copy2")
    @patch("shutil.copytree")
    @patch("pathlib.Path.glob")
    @patch("pathlib.Path.exists")
    def test_fyaml_c_installer_install(self, mock_exists, mock_glob, mock_copytree, 
                                      mock_copy2, mock_chdir, mock_clone, mock_run):
        """Test FYAML-C installer install method"""
        # Setup
        fyaml_c_version = self.setup_fyaml_c_config()
        mock_clone.return_value = True
        mock_run.return_value = None
        
        # Mock Path.exists
        mock_exists.return_value = True
        
        # Mock Path.glob to return some test files
        mock_so_files = [MagicMock(spec=Path) for _ in range(2)]
        mock_so_files[0].name = "libfyaml.so"
        mock_so_files[1].name = "libfyaml_c.so"
        
        mock_module_files = [MagicMock(spec=Path) for _ in range(2)]
        mock_module_files[0].is_file.return_value = True
        mock_module_files[0].name = "fyaml.mod"
        mock_module_files[1].is_file.return_value = True
        mock_module_files[1].name = "fyaml_c.mod"
        
        def mock_glob_side_effect(pattern):
            if pattern == "*.so":
                return mock_so_files
            elif pattern == "*":
                return mock_module_files
            return []
        
        mock_glob.side_effect = mock_glob_side_effect
        
        # Create installer
        installer = FyamlCInstaller(self.config, self.env)
        
        # Override the source_dir before prepare to avoid removal
        installer.source_dir = str(Path(self.build_dir) / "fyaml_c")
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        build_dir = source_dir / "build"
        build_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / "modules").mkdir(parents=True, exist_ok=True)
        (build_dir / "src").mkdir(parents=True, exist_ok=True)
        (build_dir / "_deps" / "libyaml-build").mkdir(parents=True, exist_ok=True)
        
        # Now call prepare but prevent rmtree from being called
        with patch("shutil.rmtree") as mock_rmtree:
            installer.prepare()
        
        # Mock downloading, configuring, and building
        installer.download()
        mock_run.reset_mock()  # Reset after previous steps
        
        # Test install method
        installer.install()
        
        # Verify copy operations for modules and libraries
        assert mock_copy2.call_count >= 3  # At least one for each .so file and libyaml.so
    
    @patch("ccs_dep.installers.fyaml_c.FyamlCInstaller.prepare")
    @patch("ccs_dep.installers.fyaml_c.FyamlCInstaller.download")
    @patch("ccs_dep.installers.fyaml_c.FyamlCInstaller.configure")
    @patch("ccs_dep.installers.fyaml_c.FyamlCInstaller.build")
    @patch("ccs_dep.installers.fyaml_c.FyamlCInstaller.install")
    @patch("ccs_dep.installers.fyaml_c.FyamlCInstaller.cleanup")
    def test_fyaml_c_installer_run(self, mock_cleanup, mock_install, mock_build, 
                                  mock_configure, mock_download, mock_prepare):
        """Test FYAML-C installer run method"""
        # Setup
        fyaml_c_version = self.setup_fyaml_c_config()
        
        # Create installer
        installer = FyamlCInstaller(self.config, self.env)
        
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
    
    @patch("ccs_dep.installers.fyaml_c.run_command")
    @patch("pathlib.Path.exists")
    @patch("shutil.copy2")
    @patch("pathlib.Path.glob")
    @patch("os.chdir")
    def test_fyaml_c_installer_install_fallback(self, mock_chdir, mock_glob, 
                                              mock_copy2, mock_exists, mock_run):
        """Test FYAML-C installer install method with fallback to cmake install"""
        # Setup
        fyaml_c_version = self.setup_fyaml_c_config()
        
        # Instead of using side_effect, we'll patch the specific calls
        # First set the default behavior
        mock_exists.return_value = True
        
        # We'll directly patch the libyaml.so check later in the test
        
        # Mock Path.glob to return some test files
        mock_so_files = [MagicMock(spec=Path) for _ in range(2)]
        mock_so_files[0].name = "libfyaml.so"
        mock_so_files[1].name = "libfyaml_c.so"
        
        mock_module_files = [MagicMock(spec=Path) for _ in range(2)]
        mock_module_files[0].is_file.return_value = True
        mock_module_files[0].name = "fyaml.mod"
        mock_module_files[1].is_file.return_value = True
        mock_module_files[1].name = "fyaml_c.mod"
        
        def mock_glob_side_effect(pattern):
            if pattern == "*.so":
                return mock_so_files
            elif pattern == "*":
                return mock_module_files
            return []
        
        mock_glob.side_effect = mock_glob_side_effect
        
        # Create installer
        installer = FyamlCInstaller(self.config, self.env)
        
        # Override the source_dir before prepare to avoid removal
        installer.source_dir = str(Path(self.build_dir) / "fyaml_c")
        
        # Create a fake source directory for testing
        source_dir = Path(installer.source_dir)
        source_dir.mkdir(parents=True, exist_ok=True)
        build_dir = source_dir / "build"
        build_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / "modules").mkdir(parents=True, exist_ok=True)
        (build_dir / "src").mkdir(parents=True, exist_ok=True)
        (build_dir / "_deps" / "libyaml-build").mkdir(parents=True, exist_ok=True)
        
        # Now call prepare but prevent rmtree from being called
        with patch("shutil.rmtree") as mock_rmtree:
            installer.prepare()
        
        # Now we need to make the libyaml.so check fail
        # Set up a temporary return_value modification for the libyaml.so check
        original_return_value = mock_exists.return_value
        mock_exists.return_value = False  # Make the libyaml.so check fail
        
        # Test install method
        installer.install()
        
        # Reset the mock to its original behavior
        mock_exists.return_value = original_return_value
        
        # Verify cmake install was called as fallback
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        assert cmd[0] == "cmake"
        assert cmd[1] == "--install"
        assert cmd[2] == "."