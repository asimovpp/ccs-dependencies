#!/usr/bin/env python3
"""
Test cases for Python dependencies installer
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from ccs_dep.installers.python_deps import PythonDepsInstaller
from tests.test_installers_base import BaseInstallerTest


class TestPythonDepsInstaller(BaseInstallerTest):
    """
    Test cases for Python dependencies installer
    """
    
    def setup_python_deps_config(self):
        """Set up Python dependencies-specific configuration and environment variables"""
        # Update environment variables
        self.env_vars["PYTHON_DEPS"] = str(self.install_dir / "python_deps")
        
        # Update configuration
        self.config["dependencies"]["python_deps"] = {
            "packages": ["pyyaml", "lit", 'flinter', 'fprettify']
        }
        
    def test_python_deps_installer_prepare(self):
        """Test Python dependencies installer prepare method"""
        # Setup
        self.setup_python_deps_config()
        
        # Create installer
        installer = PythonDepsInstaller(self.config, self.env)
        
        # Test prepare method
        installer.prepare()
        
        # Verify directories were created
        self.assert_directory_exists(installer.build_dir)
        self.assert_directory_exists(installer.dep_install_dir)
        
        # Verify expected values
        assert installer.name == "python_deps"
        assert installer.dependencies == ["pyyaml", "lit", 'flinter', 'fprettify']
    
    def test_python_deps_installer_download(self):
        """Test Python dependencies installer download method"""
        # Setup
        self.setup_python_deps_config()
        
        # Create installer
        installer = PythonDepsInstaller(self.config, self.env)
        installer.prepare()
        
        # Test download method (should be a no-op)
        installer.download()
    
    @patch("ccs_dep.installers.python_deps.venv.create")
    def test_python_deps_installer_configure(self, mock_create):
        """Test Python dependencies installer configure method"""
        # Setup
        self.setup_python_deps_config()
        mock_create.return_value = None
        
        # Create installer
        installer = PythonDepsInstaller(self.config, self.env)
        installer.prepare()
        
        # Test configure method
        installer.configure()
        
        # Verify venv.create was called correctly
        mock_create.assert_called_once()
        args, kwargs = mock_create.call_args
        # Check that the installation directory is used (could be python_deps or pythondeps-gnu)
        assert str(self.install_dir) in str(args[0])
        assert kwargs["with_pip"] is True
    
    def test_python_deps_installer_build(self):
        """Test Python dependencies installer build method"""
        # Setup
        self.setup_python_deps_config()
        
        # Create installer
        installer = PythonDepsInstaller(self.config, self.env)
        installer.prepare()
        
        # Test build method (should be a no-op)
        installer.build()
    
    @patch("ccs_dep.installers.python_deps.run_command")
    @patch("ccs_dep.installers.python_deps.open", new_callable=mock_open)
    @patch("ccs_dep.installers.python_deps.os.chmod")
    def test_python_deps_installer_install(self, mock_chmod, mock_file, mock_run):
        """Test Python dependencies installer install method"""
        # Setup
        self.setup_python_deps_config()
        mock_run.return_value = None
        
        # Create installer
        installer = PythonDepsInstaller(self.config, self.env)
        
        # Override the source_dir before prepare to avoid removal
        installer.source_dir = str(Path(self.build_dir) / "python_deps")
        
        # Now call prepare but prevent rmtree from being called
        with patch("shutil.rmtree") as mock_rmtree:
            installer.prepare()
        
        # Mock pip path determination
        with patch("sys.platform", "linux"):
            # Test install method
            installer.install()
        
        # Verify run_command calls for pip upgrade and package installation
        assert mock_run.call_count >= 3  # At least pip upgrade + two packages
        
        # Check pip upgrade call
        upgrade_call = mock_run.call_args_list[0]
        assert "pip" in upgrade_call[0][0][0]
        assert "upgrade" in upgrade_call[0][0][2]
        assert "pip" in upgrade_call[0][0][3]
        
        # Check package install calls
        pyyaml_call = mock_run.call_args_list[1]
        assert "pip" in pyyaml_call[0][0][0]
        assert "install" in pyyaml_call[0][0][1]
        assert "pyyaml" in pyyaml_call[0][0][2]
        
        lit_call = mock_run.call_args_list[2]
        assert "pip" in lit_call[0][0][0]
        assert "install" in lit_call[0][0][1]
        assert "lit" in lit_call[0][0][2]
        
        # Verify activation scripts were created
        assert mock_file.call_count == 2  # Two activation scripts
        
        # Verify chmod calls
        assert mock_chmod.call_count == 2  # Two chmod calls for scripts
    
    def test_python_deps_installer_cleanup(self):
        """Test Python dependencies installer cleanup method"""
        # Setup
        self.setup_python_deps_config()
        
        # Create installer
        installer = PythonDepsInstaller(self.config, self.env)
        installer.prepare()
        
        # Test cleanup method (should be a no-op)
        installer.cleanup()
    
    @patch("ccs_dep.installers.python_deps.PythonDepsInstaller.prepare")
    @patch("ccs_dep.installers.python_deps.PythonDepsInstaller.download")
    @patch("ccs_dep.installers.python_deps.PythonDepsInstaller.configure")
    @patch("ccs_dep.installers.python_deps.PythonDepsInstaller.build")
    @patch("ccs_dep.installers.python_deps.PythonDepsInstaller.install")
    @patch("ccs_dep.installers.python_deps.PythonDepsInstaller.cleanup")
    def test_python_deps_installer_run(self, mock_cleanup, mock_install, mock_build, 
                                    mock_configure, mock_download, mock_prepare):
        """Test Python dependencies installer run method"""
        # Setup
        self.setup_python_deps_config()
        
        # Create installer
        installer = PythonDepsInstaller(self.config, self.env)
        
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