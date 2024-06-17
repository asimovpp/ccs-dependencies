set -e


source setup_$CMP.sh

INSTALL_DIR=$PETSC
cd $BUILD_DIR

git clone --depth 1 --branch v$PETSC_VERSION https://github.com/petsc/petsc.git
cd petsc
export PETSC_DIR=$(pwd)

./configure --download-fblaslapack=yes --with-cc=${CC} --with-fc=${FC} --with-cxx=${CXX} --with-fortran-datatypes=1 --with-fortran-interfaces=1 --with-fortran-bindings=1 --with-fortran-kernels=1 --with-debugging=1 --prefix=$INSTALL_DIR
make -j 16
make install

cd ..
rm -rf petsc

