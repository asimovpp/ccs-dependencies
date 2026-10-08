set -e

source ${PWD}/setup_${ENV}.sh
INSTALL_DIR=$PARHIP_COL
cd $BUILD_DIR

git clone --depth 1 --branch mpi-collective https://github.com/eessmann/KaHIP.git
cd KaHIP

cmake --preset cirrus-gnu-release -D CMAKE_INSTALL_LIBDIR=lib
cmake --build --preset build-cirrus-gnu-release
cmake --install out/build/cirrus-gnu-release/ --prefix=$INSTALL_DIR

cd ../..
rm -rf KaHIP
