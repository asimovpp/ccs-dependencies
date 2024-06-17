set -e

source setup_$ENV.sh
INSTALL_DIR=$PARHIP
cd $BUILD_DIR

git clone --depth 1 --branch v$PARHIP_VERSION https://github.com/KaHIP/KaHIP.git parhip
cd parhip
mkdir build
cd build
CC=${CC} cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR ..
make -j 16
make install

cd ../..
rm -rf parhip
