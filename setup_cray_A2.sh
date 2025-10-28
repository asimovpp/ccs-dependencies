
export CMP=cray
source "$(dirname ${BASH_SOURCE[0]:-$0})"/setup_base.sh $1

module load PrgEnv-cray craype-network-ofi craype-x86-rome
module load cray-python
#module load cray-hdf5-parallel
#module load petsc
module load cmake
module list

export CXX=CC
export CC=cc
export FC=ftn

## PETSC build options (based on https://github.com/ARCHER2-HPC/pe-scripts/blob/master/sh/petsc.sh)
level1_dcache_assoc=4
level1_dcache_linesize=64
level1_dcache_size=16384
mpi_long_double=1
OMPFLAG="-fopenmp"
FOMPFLAG=${OMPFLAG}
FFLAGS="-O3" # -ffastmath"
ARCHFLAGS="-march=x86-64"
CFLAGS="${FFLAGS} ${ARCHFLAGS}"
FFLAGS="${FFLAGS} ${ARCHFLAGS}"
CRAY_CPU_TARGET=x86_64
PE_LIBS="-lgfortran -lgcc"
PETSC_DBG=0 # 0:release, 1:debug
PETSC_OPT=--with-debugging=${PETSC_DBG}
PETSC_OPT="${PETSC_OPT} --known-has-attribute-aligned=1"
PETSC_OPT="${PETSC_OPT} --known-mpi-int64_t=0"
PETSC_OPT="${PETSC_OPT} --known-bits-per-byte=8"
PETSC_OPT="${PETSC_OPT} --known-64-bit-blas-indices=0"
PETSC_OPT="${PETSC_OPT} --known-sdot-returns-double=0"
PETSC_OPT="${PETSC_OPT} --known-snrm2-returns-double=0"
PETSC_OPT="${PETSC_OPT} --known-level1-dcache-assoc=${level1_dcache_assoc:-4}"
PETSC_OPT="${PETSC_OPT} --known-level1-dcache-linesize=${level1_dcache_linesize:-64}"
PETSC_OPT="${PETSC_OPT} --known-level1-dcache-size=${level1_dcache_size:-16384}"
PETSC_OPT="${PETSC_OPT} --known-memcmp-ok=1"
PETSC_OPT="${PETSC_OPT} --known-mpi-c-double-complex=1"
PETSC_OPT="${PETSC_OPT} --known-mpi-long-double=$mpi_long_double"
PETSC_OPT="${PETSC_OPT} --known-mpi-shared-libraries=0"
PETSC_OPT="${PETSC_OPT} --known-sizeof-MPI_Comm=4"
PETSC_OPT="${PETSC_OPT} --known-sizeof-MPI_Fint=4"
PETSC_OPT="${PETSC_OPT} --known-sizeof-char=1"
PETSC_OPT="${PETSC_OPT} --known-sizeof-double=8"
PETSC_OPT="${PETSC_OPT} --known-sizeof-float=4"
PETSC_OPT="${PETSC_OPT} --known-sizeof-int=4"
PETSC_OPT="${PETSC_OPT} --known-sizeof-long-long=8"
PETSC_OPT="${PETSC_OPT} --known-sizeof-long=8"
PETSC_OPT="${PETSC_OPT} --known-sizeof-short=2"
PETSC_OPT="${PETSC_OPT} --known-sizeof-size_t=8"
PETSC_OPT="${PETSC_OPT} --known-sizeof-void-p=8"
PETSC_OPT="${PETSC_OPT} --with-ar=ar"
PETSC_OPT="${PETSC_OPT} --with-batch=1"
PETSC_OPT="${PETSC_OPT} --with-clib-autodetect=0"
PETSC_OPT="${PETSC_OPT} --with-cxxlib-autodetect=0"

export PETSC_OPT
