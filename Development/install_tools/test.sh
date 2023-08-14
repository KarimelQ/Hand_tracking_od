#!/bin/bash
set -e

usage()
{
    echo "usage: ./test.sh [options]"
    echo "options:"
    echo "  --miniconda_folder: path to the miniconda3 folder to be used (optional, miniconda3 by default)"
}

MINICONDA_FOLDER="miniconda3"

while [ "$1" != "" ]; do
    case $1 in
        -m | --miniconda_folder )           
            shift
            MINICONDA_FOLDER="$1"
            ;;
        -h | --help )
            usage
            exit
            ;;
        * )                     
            usage
            exit 1
            ;;
    esac
    shift
done

## Pre-commit hook
source ~/.profile
# pre-commit run --all-files

# Run the tests, assuming the build.sh script was run.
. "$MINICONDA_FOLDER"/etc/profile.d/conda.sh
conda deactivate

## Run unit tests.
conda activate tf_od
python -m pytest tests
conda deactivate
