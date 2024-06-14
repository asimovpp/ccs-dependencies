set -e

source setup_$CMP.sh

INSTALL_DIR=$HDF5_ROOT
cd $BUILD_DIR

git clone https://github.com/HDFGroup/hdf5.git
cd hdf5
git checkout tags/hdf5-1_12_1

./configure --enable-parallel --prefix=$INSTALL_DIR
make -j 16
make install

cd ..
rm -rf hdf5
