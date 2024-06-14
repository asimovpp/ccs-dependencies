set -e

source setup_${CMP}.sh
module unload petsc
unset HDF5_ROOT
unset HDF5_DIR

unset PETSC_ROOT
unset PETSC_DIR

INSTALL_DIR=$FYAMLC
cd $BUILD_DIR

git clone --depth 1 https://github.com/Nicholaswogan/fortran-yaml-c.git fyaml
cd fyaml

mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=${INSTALL_DIR} -DBUILD_SHARED_LIBS=Yes ..
cmake --build .
cmake --install .

cd ../..
rm -rf fyaml
