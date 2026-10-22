#!/bin/bash
export CMP=gnu
export PATH=/home/shared/install/openmpi-4.1.0-gnu/bin:$PATH
export LD_LIBRARY_PATH=/home/shared/install/openmpi-4.1.0-gnu/lib:$LD_LIBRARY_PATH
source "$(dirname ${BASH_SOURCE[0]:-$0})"/setup_base.sh

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
