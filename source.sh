for f in $(dirname $0)/zshfunc/*;
do source $f
done

export TERMINFO=/usr/share/terminfo/x
