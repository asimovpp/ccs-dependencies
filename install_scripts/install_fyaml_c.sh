#!/usr/bin/env bash

set -e

source setup_${ENV}.sh
unset HDF5_ROOT
unset HDF5_DIR
unset PETSC_ROOT
unset PETSC_DIR

INSTALL_DIR=$FYAMLC
cd $BUILD_DIR

git clone --depth 1 --branch v$FYAMLC_VERSION https://github.com/Nicholaswogan/fortran-yaml-c.git fyaml
cd fyaml

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} -DBUILD_SHARED_LIBS=Yes ..
cmake --build .

mkdir -p $INSTALL_DIR/{include,lib}
cp -r modules $INSTALL_DIR/
cp src/*so $INSTALL_DIR/lib/
cp _deps/libyaml-build/libyaml.so $INSTALL_DIR/lib
#cmake --install .

cd ../..
rm -rf fyaml
