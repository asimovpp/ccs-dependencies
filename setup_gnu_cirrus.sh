
export CMP=gnu
source "$(dirname ${BASH_SOURCE[0]:-$0})"/setup_base.sh

module load python
module load cmake
module load bison
module load flex
module load gcc
module load openmpi

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
