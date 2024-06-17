set -e

# Setup
source setup_${ENV}.sh

INSTALL_DIR=${RCMF90}
cd $BUILD_DIR

# Get code
git clone --depth 1 git@git.ecdf.ed.ac.uk:asimov/rcm-f90.git rcm-f90
cd rcm-f90

# Build
make CMP=${CMP/_*/}

# Install
mkdir -p ${INSTALL_DIR}
cp -r lib ${INSTALL_DIR}/
cp -r include ${INSTALL_DIR}/

# Clean up
cd ../
rm -rf rcm-f90
