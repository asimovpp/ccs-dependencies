
export CMP=gnu
source setup_base.sh

module load python
module load cmake
module load bison
module load flex
module load gcc
module load openmpi

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
