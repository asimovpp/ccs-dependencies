
export CMP=gnu
source "$(dirname ${BASH_SOURCE[0]:-$0})"/setup_base.sh

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
