set -e

source ${PWD}/setup_${ENV}.sh

INSTALL_DIR=$LIKWID
cd $BUILD_DIR

wget http://ftp.fau.de/pub/likwid/likwid-$LIKWID_VERSION.tar.gz
tar -xaf likwid-$LIKWID_VERSION.tar.gz
cd likwid-$LIKWID_VERSION

sed -i "s/FC  = ifx/FC  = ftn/" make/include_GCC.mk
sed -i "/^FCFLAGS/d" make/include_GCC.mk
sed -i "s/^#FCFLAGS/FCFLAGS/" make/include_GCC.mk

make PREFIX=$INSTALL_DIR FORTRAN_INTERFACE=true ACCESSMODE=direct
make PREFIX=$INSTALL_DIR FORTRAN_INTERFACE=true ACCESSMODE=direct install


