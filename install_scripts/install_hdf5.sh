#!/usr/bin/env bash

set -e

source setup_$ENV.sh

INSTALL_DIR=$HDF5_ROOT
cd $BUILD_DIR

git clone --depth 1 --branch hdf5_$HDF5_VERSION https://github.com/HDFGroup/hdf5.git
cd hdf5

./configure --enable-parallel --prefix=$INSTALL_DIR
make -j 16
make install

cd ..
rm -rf hdf5
