set -e

source setup_$CMP.sh
INSTALL_DIR=$PARHIP
cd $BUILD_DIR

git clone https://github.com/KaHIP/KaHIP.git parhip
cd parhip
git checkout tags/v3.14
mkdir build
cd build
CC=${CC} cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR ..
make -j 16
make install

cd ../..
rm -rf parhip
