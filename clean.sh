#!/bin/bash

# Removes symlinks set by ./deploy.sh
DIR=$(dirname $0)

for CONF in $(ls $DIR/config); do
    rm -rf "/home/$USER/.config/$CONF";
done

for CONF in $(ls $DIR/home); do
    rm "/home/$USER/.$CONF";
done

echo "Done!!!"
echo " To check symlinks from home directory, Try running "
echo "$ lsd -la --recursive --depth 2 | grep lrw | grep Dropbox"
