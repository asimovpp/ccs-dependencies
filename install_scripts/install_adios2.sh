set -e

source setup_$ENV.sh

INSTALL_DIR=$ADIOS2
cd $BUILD_DIR

git clone --depth 1 --branch v$ADIOS2_VERSION https://github.com/ornladios/ADIOS2.git adios2
cd adios2
mkdir build
cd build
cmake -DCMAKE_C_COMPILER=${CC} \
    -DCMAKE_CXX_COMPILER=${CXX} \
    -DCMAKE_Fortran_COMPILER=${FC} \
    -DADIOS2_USE_SST=OFF \
    -DADIOS2_USE_Fortran=ON \
    -DADIOS2_USE_MPI=ON \
    -DADIOS2_USE_HDF5=ON \
    -DHDF5_ROOT=$HDF5_ROOT \
    -DADIOS2_USE_Python=OFF \
    -DADIOS2_USE_ZeroMQ=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR ..
make -j 16
make install

cd ../..
rm -rf adios2
