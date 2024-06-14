#!/bin/bash
export CMP=gnu_cirrus

source setup_$CMP.sh

bash install_scripts/install_hdf5.sh
source install_base.sh
bash install_scripts/install_petsc.sh
