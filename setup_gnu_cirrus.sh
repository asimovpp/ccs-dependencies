
export CMP=gnu
source setup_base.sh

module load cmake
module load bison
module load gcc
module load openmpi

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
