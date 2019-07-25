#!/bin/bash

# Removes symlinks set by ./deploy.sh
DIR=$(dirname $0)


# Source the path pairs to use while deploying
source $DIR/pairs.sh

for paths in ${PATH_PAIRS[@]}; do
    IFS="," read src dest dot <<<"${paths}";
    for file in $(ls $src); do
        rm -rf "$dest/$dot$file";
    done
done

echo "Done!!!"
echo " To check symlinks from home directory, Try running "
echo "$ lsd -la --recursive --depth 2 | grep lrw | grep Dropbox"

DIR=$PWD
cd ~/ && lsd -la --recursive --depth 2 | grep lrw | grep Dropbox && cd $DIR
