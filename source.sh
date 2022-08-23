for f in $(dirname $0)/zshfunc/*;
do source $f
done

export TERMINFO=/usr/share/terminfo
export PATH=~/.local/bin:$PATH

intersection () {
    comm -12 <(sort $1) <(sort $2)
}
