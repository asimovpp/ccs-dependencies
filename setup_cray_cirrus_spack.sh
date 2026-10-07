
export CMP=cray
source "$(dirname ${BASH_SOURCE[0]:-$0})"/setup_base.sh

module load PrgEnv-cray craype-network-ofi craype-x86-turin
module load cray-python
#module load cray-hdf5-parallel
#module load petsc
#module load cmake
module load spack
module list

export CC=cc
export CXX=CC
export FC=ftn


bash install_scripts/install_python_pyyaml_lit.sh
spack install makedepf90 %cce_all
spack install libfyaml %cce_all
spack install hdf5+mpi+fortran %cce_all
spack install adios2+hdf5 %cce_all
spack install petsc+debug %cce_all
spack install parhip %cce_all
bash install_scripts/install_parhip.sh
spack install parmetis %cce_all
spack install parmetis+int64 %cce_all
bash install_scripts/install_rcm_f90.sh
spack install caliper+fortran %cce_all
