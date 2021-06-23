for f in $(dirname $0)/zshfunc/*;
do source $f
done

export TERMINFO=/etc/terminfo
export PATH=~/.local/bin:$PATH
