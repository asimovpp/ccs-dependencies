set -e

source ${PWD}/setup_${ENV}.sh

INSTALL_DIR=$HDF5_ROOT
cd $BUILD_DIR

git clone --depth 1 --branch $HDF5_VERSION https://github.com/HDFGroup/hdf5.git
cd hdf5

# ./configure --enable-parallel --enable-subfiling-vfd=yes --prefix=$INSTALL_DIR

mkdir -p build && cd build
# config
cmake -DCMAKE_BUILD_TYPE=Release \
      -DHDF5_ENABLE_PARALLEL=ON \
      -DBUILD_SHARED_LIBS=ON \
      -DHDF5_ENABLE_SUBFILING_VFD=OFF \
      ..

# compile
cmake --build . --config Release -j 16
#install
cmake --install . --prefix $INSTALL_DIR

cd $BUILD_DIR
rm -rf hdf5
