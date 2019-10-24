#!/bin/bash

DIR=$(dirname $0)

# Source the path pairs to use while deploying
source $DIR/pairs.sh

for paths in ${PATH_PAIRS[@]}; do
    IFS="," read src dest dot <<<"${paths}";
    for file in $(ls $src); do
        ln -s "$src/$file" "$dest/$dot$file";
    done
done

echo "Done!!!"
echo " To check symlinks from home directory, Try running "
echo "$ ls -la --recursive | grep lrw | grep dotfiles"

DIR=$PWD
cd ~/ && lsd -la --recursive | grep lrw | grep dotfiles && cd $DIR
