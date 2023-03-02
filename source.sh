for f in $(dirname $0)/zshfunc/*;
do source $f
done

# Add .local/bin to PATH
[ -d ~/.local/bin ] && export PATH=~/.local/bin:$PATH


# set nvim as default vim if available
[[ -x $(command -v nvim) ]] && alias vim=nvim
