for f in $(dirname $0)/zshfunc/*;
do source $f
done

# Add .local/bin to PATH
[ -d ~/.local/bin ] && export PATH=~/.local/bin:$PATH

# Add findutils if available
# On mac, this helps with getting gnu find as find instead of gfind
# Installed with `brew install findutils`
[ -d /opt/homebrew/opt/findutils/libexec/gnubin ] && export PATH=/opt/homebrew/opt/findutils/libexec/gnubin:$PATH


