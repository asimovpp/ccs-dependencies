# ccs-dependencies
Set of scripts to build CCS dependencies on various systems


## Build dependencies

- First setup the `INSTALL_DIR` and `BUILD_DIR` variables in `setup_base.sh` for example
```Bash
INSTALL_DIR=${HOME}/ccs-libs
BUILD_DIR=/tmp/build-ccs-deps/
```

- Build and install the dependencies:
```Bash
ENV=cray_A2 ./install_base.sh
```

Set ENV according to your platform and desired build environment. The possible values each have a file named `setup_$ENV.sh` in the root folder of this repo.

## Build ccs

Once all the libraries have been installed, you just need to source the right setup script to build ccs, for example:
```Bash
export INSTALL_DIR=${HOME}/ccs-libs # Set to ccs-dependencies install location
source setup_cray_A2.sh

git clone git@github.com:asimovpp/asimov-ccs.git
cd  asimov-ccs
make all
```
