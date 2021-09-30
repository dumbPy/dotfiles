
# user kitty as the default terminal
# TERM="xterm-kitty"
# TERM="xterm-256color"
# use firefox as default browser
BROWSER="brave-browser"
EDITOR="vim"

alias ftp_up="sudo docker run -d -p 20-21:20-21 -p 65500-65515:65500-65515 --name ftp -v ~/applications/ftp:/var/ftp:ro metabrainz/docker-anon-ftp"
alias ftp_down="sudo docker rm -f ftp"

alias sudo="sudo " # to enable sudo before alias
alias ec="emacsclient -c --a $EDITOR " # open in emacsclient gui if emacs daemon is running else open in default editor (vim)
