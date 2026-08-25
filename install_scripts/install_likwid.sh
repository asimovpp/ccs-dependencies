set -e

source ${PWD}/setup_${ENV}.sh

INSTALL_DIR=$LIKWID
cd $BUILD_DIR

# defaults
export lik_cmp="GCC"
export CC=gcc
export FC=ifort
export FCFLAGS="-module ./"

if [ "$CMP" = "cray" ]; then
	export lik_cmp=CLANG
	export CC=cc
	export FC=ftn
	export FCFLAGS="-ef -J ./"
elif [ "$CMP" = "gnu" ]; then
	export lik_cmp=GCC
	export CC=cc
	export FC=ftn
	export FCFLAGS="-J ./ -fsyntax-only"
fi

wget http://ftp.fau.de/pub/likwid/likwid-$LIKWID_VERSION.tar.gz
tar -xaf likwid-$LIKWID_VERSION.tar.gz
cd likwid-$LIKWID_VERSION

make COMPILER=$lik_cmp CC=$CC FC=$FC FCFLAGS="$FCFLAGS" PREFIX=$INSTALL_DIR FORTRAN_INTERFACE=true ACCESSMODE=direct
make COMPILER=$lik_cmp CC=$CC FC=$FC FCFLAGS="$FCFLAGS" PREFIX=$INSTALL_DIR FORTRAN_INTERFACE=true ACCESSMODE=direct install
