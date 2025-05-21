#!/usr/bin/env python3
"""
Main installation script for CCS dependencies
"""
import argparse
import os
import sys
import yaml
import logging
import importlib
import importlib.util
from pathlib import Path
from utils.environment import Environment
from utils.system import detect_system


def main():
    """
    Main function for the CCS dependencies installer.
    
    This can be run directly or as a Poetry entry point with: ccs-install
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Install CCS dependencies")
    parser.add_argument("--env", default=None, help="Environment name (e.g., gnu_ubuntu, gnu_macos)")
    parser.add_argument("--config", default=None, help="Path to custom configuration file")
    parser.add_argument("--install-dir", default=None, help="Installation directory")
    parser.add_argument("--build-dir", default=None, help="Build directory")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--dependencies", default=None, help="Comma-separated list of dependencies to install")
    parser.add_argument("--version", action="store_true", help="Show version information")
    args = parser.parse_args()
    
    # Show version info if requested
    if args.version:
        show_version_info()
        return
    
    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level, 
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Check for Poetry environment
    check_poetry_environment()
    
    # Detect system if environment not specified
    env_name = args.env
    if not env_name:
        env_name = detect_system()
        logging.info(f"Detected environment: {env_name}")
    
    # Load configuration
    config = load_configuration(env_name, args.config)
    
    # Override with command line arguments
    if args.install_dir:
        config["install_dir"] = args.install_dir
    if args.build_dir:
        config["build_dir"] = args.build_dir
    
    # Set up environment
    env = Environment(env_name, config)
    env.apply()
    
    # Print environment information
    env.print_environment()
    
    # Create install and build directories
    os.makedirs(env.get_install_dir(), exist_ok=True)
    os.makedirs(env.get_build_dir(), exist_ok=True)
    
    # Determine which dependencies to install
    all_deps = config.get("installation_order", [])
    deps_to_install = all_deps
    if args.dependencies:
        deps_to_install = args.dependencies.split(",")
        # Validate dependencies
        for dep in deps_to_install:
            if dep not in all_deps:
                logging.error(f"Unknown dependency: {dep}")
                logging.error(f"Available dependencies: {', '.join(all_deps)}")
                sys.exit(1)
    
    # Install dependencies
    results = {}
    for dep in deps_to_install:
        logging.info(f"Installing {dep}...")
        try:
            # Dynamically import installer module
            try:
                installer_module = importlib.import_module(f"installers.{dep}")
                # Get the installer class name (capitalize the dependency name)
                class_name = "".join(word.capitalize() for word in dep.split("_")) + "Installer"
                installer_class = getattr(installer_module, class_name)
                installer = installer_class(config, env)
                success = installer.run()
                results[dep] = "SUCCESS" if success else "FAILED"
            except (ImportError, AttributeError) as e:
                logging.error(f"Installer module not found for {dep}: {e}")
                results[dep] = "MISSING"
        except Exception as e:
            logging.error(f"Error installing {dep}: {e}")
            results[dep] = "ERROR"
    
    # Print summary
    logging.info("Installation summary:")
    for dep, status in results.items():
        logging.info(f"  {dep}: {status}")


def show_version_info():
    """
    Display version information for the CCS dependencies installer
    """
    # Try to get version from pyproject.toml using Poetry metadata
    try:
        from importlib.metadata import version
        print(f"CCS Dependencies Installer v{version('ccs-dependencies')}")
    except (ImportError, ModuleNotFoundError):
        # Fallback if not installed with Poetry
        print("CCS Dependencies Installer")
    
    print("Python version:", sys.version)
    print("Platform:", sys.platform)


def check_poetry_environment():
    """
    Check if running in a Poetry environment and verify dependencies are available
    """
    # Verify required packages are available
    required_packages = ["yaml"]
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            logging.warning(f"Required package '{package}' not found.")
            logging.warning("Consider using Poetry to manage dependencies:")
            logging.warning("  poetry install")
            logging.warning("  poetry run ccs-install")


def load_configuration(env_name, custom_config=None):
    """
    Load configuration for the specified environment
    
    Args:
        env_name (str): Environment name
        custom_config (str, optional): Path to custom configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    # Current script directory - handle both direct execution and installed package
    try:
        # If running as an installed package
        import ccs_dependencies
        package_dir = Path(ccs_dependencies.__file__).parent
        config_dir = package_dir / "config"
    except ImportError:
        # If running directly from source
        script_dir = Path(__file__).parent
        config_dir = script_dir / "config"
    
    # Load default configuration
    default_config_path = config_dir / "default_config.yml"
    if not default_config_path.exists():
        logging.error(f"Default configuration file not found: {default_config_path}")
        sys.exit(1)
    
    with open(default_config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Load environment-specific configuration
    env_config_path = config_dir / f"{env_name}.yml"
    if env_config_path.exists():
        with open(env_config_path, "r") as f:
            env_config = yaml.safe_load(f)
            # Merge configurations
            config = merge_configs(config, env_config)
    else:
        logging.warning(f"Environment-specific configuration not found: {env_config_path}")
    
    # Load custom configuration if specified
    if custom_config and os.path.exists(custom_config):
        with open(custom_config, "r") as f:
            custom_config_data = yaml.safe_load(f)
            # Merge configurations
            config = merge_configs(config, custom_config_data)
    
    return config


def merge_configs(base_config, override_config):
    """
    Recursively merge two configuration dictionaries
    
    Args:
        base_config (dict): Base configuration
        override_config (dict): Override configuration
        
    Returns:
        dict: Merged configuration
    """
    result = base_config.copy()
    for key, value in override_config.items():
        if (
            key in result and 
            isinstance(result[key], dict) and 
            isinstance(value, dict)
        ):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result


if __name__ == "__main__":
    main()