#!/bin/bash
set -e

export CMP=${ENV/_*/}
source setup_$ENV.sh

mkdir -p $BUILD_DIR
mkdir -p $INSTALL_DIR

bash install_scripts/install_makedepf90.sh
bash install_scripts/install_fyaml_c.sh
bash install_scripts/install_hdf5.sh
bash install_scripts/install_adios2.sh
bash install_scripts/install_petsc.sh
bash install_scripts/install_parhip.sh
bash install_scripts/install_parmetis.sh
bash install_scripts/install_rcm_f90.sh
