for f in $(dirname $0)/zshfunc/*;
do source $f
done

# Add .local/bin to PATH
[ -d ~/.local/bin ] && export PATH=~/.local/bin:$PATH


