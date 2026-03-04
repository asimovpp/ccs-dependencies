set -e

source setup_${ENV}.sh

INSTALL_DIR=$LIKWID
cd $BUILD_DIR

wget http://ftp.fau.de/pub/likwid/likwid-$LIKWID_VERSION.tar.gz
tar -xaf likwid-$LIKWID_VERSION.tar.gz
cd likwid-$LIKWID_VERSION
vim make/include_GCC.mk
make PREFIX=$INSTALL_DIR FORTRAN_INTERFACE=true ACCESSMODE=direct
make PREFIX=$INSTALL_DIR FORTRAN_INTERFACE=true ACCESSMODE=direct install


