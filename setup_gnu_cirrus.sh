
export CMP=gnu
source setup_base.sh

module load gcc/10.2.0
module load openmpi/4.1.4

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
