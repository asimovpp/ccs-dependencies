
export CMP=cray
source "$(dirname ${BASH_SOURCE[0]:-$0})"/setup_base.sh

module load PrgEnv-cray craype-network-ofi craype-x86-turin
module load cray-python
#module load cray-hdf5-parallel
#module load petsc
module load cmake
module list

export CC=cc
export CXX=CC
export FC=ftn
