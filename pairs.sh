#!/bin/bash

# Source and Destination pairs for symlinks to deploy
# example, "$DIR/config","/home/$USER/.config"

# source, destination, dot
# If dot is given, the symlinked file/folder is hidden.
PATH_PAIRS=(
    "$DIR/config","/home/$USER/.config"
    "$DIR/home","/home/$USER","."
)
