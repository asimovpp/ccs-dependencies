set -e

source setup_${ENV}.sh
if [[ "$1" == "32bit" ]]
then
    INSTALL_DIR=$PARMETIS_32bit
else
    INSTALL_DIR=$PARMETIS
fi
cp patch/gklib_force_fpic.patch $BUILD_DIR/
cd $BUILD_DIR

mkdir parmetis
cd parmetis

git clone https://github.com/KarypisLab/GKlib.git gklib
cd gklib
git checkout 8bd6bad750b2b0d908
git apply ../../gklib_force_fpic.patch
make config cc=${CC} prefix=$INSTALL_DIR
make install -j16
cd ..

git clone https://github.com/KarypisLab/METIS.git metis
cd metis
if [[ "$1" == "32bit" ]]
then
    make config shared=1 cc=${CC} prefix=$INSTALL_DIR gklib_path=$INSTALL_DIR i32=1
else
    make config shared=1 cc=${CC} prefix=$INSTALL_DIR gklib_path=$INSTALL_DIR i64=1
fi
make install -j16
cd ..

git clone https://github.com/KarypisLab/ParMETIS.git parmetis
cd parmetis
make config shared=1 cc=${CC} prefix=$INSTALL_DIR gklib_path=$INSTALL_DIR metis_path=$INSTALL_DIR
make install -j16
cd ..

cd ..
rm -rf parmetis
rm $BUILD_DIR/gklib_force_fpic.patch
