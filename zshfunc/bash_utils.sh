# user kitty as the default terminal
# TERM="xterm-kitty"
# TERM="xterm-256color"
# use firefox as default browser
BROWSER="firefox"
EDITOR="vim"

# In TMUX sessions, forwarded ssh keys are not accessible. this fixes that issue
fixssh() {
eval $(tmux show-env -s |grep '^SSH_')
}
