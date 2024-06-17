set -e

source setup_$ENV.sh

INSTALL_DIR=$MAKEDEPF90
cd "$BUILD_DIR"

git clone https://salsa.debian.org/science-team/makedepf90.git

cd makedepf90
./configure --prefix=$INSTALL_DIR

make
#make install
mkdir -p $INSTALL_DIR/bin
cp makedepf90 $INSTALL_DIR/bin
cd ..
rm -rf makedepf90

