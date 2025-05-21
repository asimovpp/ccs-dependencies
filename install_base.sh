#!/bin/bash
set -e

export CMP=${ENV/_*/}
. setup_"$ENV".sh

echo "Environment: $ENV"
echo "Compiler: $CMP"
echo "Build directory: $BUILD_DIR"
echo "Install directory: $INSTALL_DIR"

mkdir -pv $BUILD_DIR
mkdir -pv $INSTALL_DIR

#bash install_scripts/install_python_pyyaml_lit.sh
bash install_scripts/install_makedepf90.sh
bash install_scripts/install_fyaml_c.sh
bash install_scripts/install_hdf5.sh
bash install_scripts/install_adios2.sh
bash install_scripts/install_petsc.sh
bash install_scripts/install_parhip.sh
bash install_scripts/install_parmetis.sh
bash install_scripts/install_rcm_f90.sh
