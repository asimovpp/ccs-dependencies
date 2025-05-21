# Python-Based CCS Dependencies Architecture

## Directory Structure

```
ccs-dependencies/
├── config/
│   ├── __init__.py
│   ├── default_config.yml       # Default configuration values
│   ├── gnu_ubuntu.yml           # Ubuntu-specific configuration
│   ├── gnu_macos.yml            # macOS-specific configuration
│   └── cray_A2.yml              # Cray-specific configuration
├── installers/
│   ├── __init__.py
│   ├── base.py                  # Base installer class
│   ├── makedepf90.py            # Individual installer modules
│   ├── fyaml_c.py
│   ├── hdf5.py
│   ├── adios2.py
│   ├── petsc.py
│   ├── parhip.py
│   ├── parmetis.py
│   ├── rcm_f90.py
│   └── python_deps.py
├── utils/
│   ├── __init__.py
│   ├── environment.py           # Environment setup utilities
│   ├── system.py                # System detection utilities
│   └── command.py               # Command execution utilities
├── install.py                   # Main installation script
├── setup.py                     # Environment setup script
├── requirements.txt             # Python dependencies
└── README.md                    # Updated documentation
```

## Key Components

### Configuration System

- YAML-based configuration files
- Environment-specific configurations inherit from default configuration
- Allows for easy addition of new environments
- Dependency versions defined in a single location

### Base Installer Class

```python
class BaseInstaller:
    def __init__(self, config, env):
        self.config = config
        self.env = env
        self.install_dir = env.get_install_dir()
        self.build_dir = env.get_build_dir()
        
    def prepare(self):
        """Prepare build environment"""
        pass
        
    def download(self):
        """Download/clone source code"""
        pass
        
    def configure(self):
        """Configure the build"""
        pass
        
    def build(self):
        """Build the software"""
        pass
        
    def install(self):
        """Install the software"""
        pass
        
    def cleanup(self):
        """Clean up the build directory"""
        pass
        
    def run(self):
        """Run the full installation process"""
        self.prepare()
        self.download()
        self.configure()
        self.build()
        self.install()
        self.cleanup()
        return True
```

### Environment Class

```python
class Environment:
    def __init__(self, env_name, config):
        self.env_name = env_name
        self.config = config
        self.env_vars = {}
        self.setup_environment()
        
    def setup_environment(self):
        """Set up environment variables based on config"""
        # Set up basic environment variables
        self.env_vars["INSTALL_DIR"] = self.config.get("install_dir", os.path.expanduser("~/ccs-deps"))
        self.env_vars["BUILD_DIR"] = self.config.get("build_dir", "/tmp/build-ccs-deps")
        # Set up compiler variables
        self.env_vars["CC"] = self.config.get("cc", "mpicc")
        self.env_vars["CXX"] = self.config.get("cxx", "mpicxx")
        self.env_vars["FC"] = self.config.get("fc", "mpifort")
        # Set up dependency-specific variables
        for dep, config in self.config.get("dependencies", {}).items():
            if "version" in config:
                self.env_vars[f"{dep.upper()}_VERSION"] = config["version"]
            if "install_dir" in config:
                self.env_vars[dep.upper()] = config["install_dir"]
                
    def get_env_vars(self):
        """Get environment variables as a dictionary"""
        return self.env_vars
        
    def get_install_dir(self):
        """Get installation directory"""
        return self.env_vars["INSTALL_DIR"]
        
    def get_build_dir(self):
        """Get build directory"""
        return self.env_vars["BUILD_DIR"]
        
    def apply(self):
        """Apply environment variables to the current process"""
        for key, value in self.env_vars.items():
            os.environ[key] = value
```

### Main Installation Script

```python
import argparse
import os
import sys
import yaml
import logging
from utils.environment import Environment
from utils.system import detect_system
import importlib

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Install CCS dependencies")
    parser.add_argument("--env", default=None, help="Environment name (e.g., gnu_ubuntu, gnu_macos)")
    parser.add_argument("--config", default=None, help="Path to custom configuration file")
    parser.add_argument("--install-dir", default=None, help="Installation directory")
    parser.add_argument("--build-dir", default=None, help="Build directory")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--dependencies", default=None, help="Comma-separated list of dependencies to install")
    args = parser.parse_args()
    
    # Configure logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
    
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
            installer_module = importlib.import_module(f"installers.{dep}")
            installer_class = getattr(installer_module, f"{dep.capitalize()}Installer")
            installer = installer_class(config, env)
            success = installer.run()
            results[dep] = "SUCCESS" if success else "FAILED"
        except Exception as e:
            logging.error(f"Error installing {dep}: {e}")
            results[dep] = "ERROR"
    
    # Print summary
    logging.info("Installation summary:")
    for dep, status in results.items():
        logging.info(f"  {dep}: {status}")

def load_configuration(env_name, custom_config=None):
    """Load configuration for the specified environment"""
    # Load default configuration
    default_config_path = os.path.join("config", "default_config.yml")
    if not os.path.exists(default_config_path):
        logging.error(f"Default configuration file not found: {default_config_path}")
        sys.exit(1)
    
    with open(default_config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Load environment-specific configuration
    env_config_path = os.path.join("config", f"{env_name}.yml")
    if os.path.exists(env_config_path):
        with open(env_config_path, "r") as f:
            env_config = yaml.safe_load(f)
            # Merge configurations
            config = merge_configs(config, env_config)
    
    # Load custom configuration if specified
    if custom_config and os.path.exists(custom_config):
        with open(custom_config, "r") as f:
            custom_config_data = yaml.safe_load(f)
            # Merge configurations
            config = merge_configs(config, custom_config_data)
    
    return config

def merge_configs(base_config, override_config):
    """Recursively merge two configuration dictionaries"""
    result = base_config.copy()
    for key, value in override_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result

if __name__ == "__main__":
    main()
```

## Example Configuration File (default_config.yml)

```yaml
# Default configuration
install_dir: ~/ccs-deps
build_dir: /tmp/build-ccs-deps

# Dependency versions
dependencies:
  adios2:
    version: 2.10.1
  parhip:
    version: 3.14
  petsc:
    version: 3.21.2
  hdf5:
    version: 1.14.4.3
  fyaml_c:
    version: 0.2.5

# Default installation order
installation_order:
  - makedepf90
  - fyaml_c
  - hdf5
  - adios2
  - petsc
  - parhip
  - parmetis
  - rcm_f90
  - python_deps

# Build options
parallel_jobs: 16
```

## Example Environment-Specific Configuration (gnu_macos.yml)

```yaml
# macOS with GNU compilers configuration
cc: mpicc
cxx: mpicxx
fc: mpifort

# Override dependency-specific settings if needed
dependencies:
  petsc:
    configure_options:
      - "--download-fblaslapack=yes"
      - "--with-fortran-datatypes=1"
      - "--with-fortran-interfaces=1"
      - "--with-fortran-bindings=1"
      - "--with-fortran-kernels=1"
      - "--with-debugging=1"
```

## Example Installer Module (hdf5.py)

```python
import os
import logging
from installers.base import BaseInstaller
from utils.command import run_command

class Hdf5Installer(BaseInstaller):
    def __init__(self, config, env):
        super().__init__(config, env)
        self.version = self.env.get_env_vars().get("HDF5_VERSION")
        self.install_dir = self.env.get_env_vars().get("HDF5_ROOT")
        self.source_dir = os.path.join(self.build_dir, "hdf5")
        
    def download(self):
        logging.info(f"Downloading HDF5 version {self.version}")
        os.chdir(self.build_dir)
        run_command(
            ["git", "clone", "--depth", "1", 
             "--branch", f"hdf5_{self.version}", 
             "https://github.com/HDFGroup/hdf5.git"]
        )
        
    def configure(self):
        logging.info("Configuring HDF5")
        os.chdir(self.source_dir)
        run_command(
            ["./configure", "--enable-parallel", f"--prefix={self.install_dir}"]
        )
        
    def build(self):
        logging.info("Building HDF5")
        os.chdir(self.source_dir)
        run_command(["make", f"-j{self.config.get('parallel_jobs', 16)}"])
        
    def install(self):
        logging.info("Installing HDF5")
        os.chdir(self.source_dir)
        run_command(["make", "install"])
        
    def cleanup(self):
        logging.info("Cleaning up HDF5 build directory")
        os.chdir(self.build_dir)
        run_command(["rm", "-rf", "hdf5"])
```