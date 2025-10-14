The basic setup (compilers and MPI library) for AMD llvm compilers is described here. Some details will need to be adapted for different systems, but the main information is here.

- Compiler is rocm-afar-7992-drop-6.2.0 which was downloaded from https://repo.radeon.com/rocm/misc/flang/
- Openmpi 5.0.8 was installed by doing:

```
set -e

INSTALL_DIR=${H}"/install/openmpi-5.0.8-aocc/"
OMPI="openmpi-5.0.8"

mkdir tmp_build
cd tmp_build

wget https://download.open-mpi.org/release/open-mpi/v5.0/${OMPI}.tar.gz
tar -xf ${OMPI}.tar.gz
cd ${OMPI}
mkdir build_min
cd build_min
../configure CFLAGS=-fPIC CXXFLAGS=-fPIC FFLAGS=-fPIC CC=amdclang CXX=amdclang++ F77=amdflang FC=amdflang --prefix=${INSTALL_DIR}
make
make install

cd ../../..
rm -rf tmp_build
```

- Environment was set up with:
```
H=/home/shared

export PATH=$H/install/aocc-compiler-6.2.0/bin:$PATH
export LIBRARY_PATH=$H/install/aocc-compiler-6.2.0/lib:$LIBRARY_PATH

export PATH=$H/install/openmpi-5.0.8-aocc/bin:$PATH
export LD_LIBRARY_PATH=$H/install/openmpi-5.0.8-aocc/lib:$LD_LIBRARY_PATH
```

