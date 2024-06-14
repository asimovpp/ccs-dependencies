#!/bin/bash

source setup_$CMP.sh
sudo apt install yacc flex
sudo apt install cmake
sudo apt install openmpi-bin libopenmpi-dev
pip install --user lit flinter fprettify pyyaml

source install_base.sh
