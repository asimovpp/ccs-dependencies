#!/bin/bash

#set -e

source setup_${ENV}.sh

INSTALL_DIR=$CALIPER
cd $BUILD_DIR

git clone --depth 1 --branch v$CALIPER_VERSION https://github.com/llnl/Caliper.git caliper
cd caliper

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} -DWITH_FORTRAN=ON -DWITH_MPI=ON ..
make
make install

cd ../..
rm -rf caliper
