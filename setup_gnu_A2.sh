

export CMP=gnu
source setup_base.sh

module load PrgEnv-gnu
module load cray-python
module load cray-hdf5-parallel
module load petsc
module load cmake
module list

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
