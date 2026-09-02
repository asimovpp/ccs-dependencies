set -e

source ${PWD}/setup_${ENV}.sh

pip install --user --upgrade pip
pip install --user pyyaml
pip install --user lit