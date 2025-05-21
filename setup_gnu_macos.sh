#!/usr/bin/env bash
# This script sets up the environment for building and running CCS dependencies on macOS using GNU compilers.
export CMP=gnu
. "${PWD}"/setup_base.sh

export CC=mpicc
export FC=mpifort
export CXX=mpicxx
