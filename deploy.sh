#!/bin/bash

DIR=$(dirname $0)

# Symlink everything from ./config folder to ~/.config
# PATH_PAIRS=(
#     "$DIR/config","/home/$USER/.config"
#     "$DIR/home","/home/$USER","."
# )
# Source the path pairs to use while deploying
source $DIR/pairs.sh

for paths in ${PATH_PAIRS[@]}; do
    IFS="," read src dest dot <<<"${paths}";
    for file in $(ls $src); do
        ln -s "$src/$file" "$dest/$dot$file";
    done
done

# for CONF in $(ls $DIR/config); do
#     ln -s "$DIR/config/$CONF" "/home/$USER/.config/$CONF";
# done
#
# # Symlink all files in ./home to ~/
# for CONF in $(ls $DIR/home); do
#     ln -s "$DIR/home/$CONF" "/home/$USER/.$CONF";
# done

echo "Done!!!"
echo " To check symlinks from home directory, Try running "
echo "$ lsd -la --recursive --depth 2 | grep lrw | grep Dropbox"

DIR=$PWD
cd ~/ && lsd -la --recursive --depth 2 | grep lrw | grep Dropbox && cd $DIR
