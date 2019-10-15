export PATH=/var/opt/anaconda3/bin:$USER/.local/bin:/var/opt/kitty/bin:$PATH
alias google='python ~/bin/googler'
alias escape_spaces="sed 's/ /\\\ /g'"
alias ftp_up="sudo docker run -d -p 20-21:20-21 -p 65500-65515:65500-65515 --name ftp -v ~/applications/ftp:/var/ftp:ro metabrainz/docker-anon-ftp"
alias ftp_down="sudo docker rm -f ftp"
alias firefox="/var/opt/python2/firefox"

alias sudo="sudo " # to enable sudo before alias

# firefox
# firefox(){
#     # open xhost to all local programs
#     xhost +local:
#     # run firefox in docker and remove it when it ends
#     sudo docker run -it --rm \
#         --env="DISPLAY" \
#         -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
#         -v "${HOME}/.Xauthority:/root/.Xauthority" \
#         -v "${HOME}/.temp/.firefox/cache:/root/.cache/mozilla" \
# 	    -v "${HOME}/.temp/.firefox/mozilla:/root/.mozilla" \
# 	    -v "${HOME}/Downloads:/root/Downloads" \
# 	    -v "${HOME}/Pictures:/root/Pictures" \
#         --name firefox \
#         jess/firefox
#     # remove xhost permissions
#     xhost -local:
#     # exit 0
# }

# xhost +local:`sudo docker inspect --format='{{ .Config.Hostname }}' $containerId`

# chrome
chrome(){
    xhost +local:
    sudo docker run -it \
        --env="DISPLAY" \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
	    -v "${HOME}/.chrome:/data" \
	    -v "${HOME}/Downloads:/root/Downloads" \
	    -v "${HOME}/Pictures:/root/Pictures" \
        --device /dev/snd:/dev/snd \
		-v /etc/hosts:/etc/hosts \
        --name chrome \
        jess/chrome --user-data-dir=/data --no-sandbox
}

spotify(){
    xhost +local:
    sudo docker run -d  \
        -v /etc/localtime:/etc/localtime:ro \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        --env="DISPLAY" \
        --device /dev/snd:/dev/snd \
        -v $HOME/.spotify/config:/home/spotify/.config/spotify \
        -v $HOME/.spotify/cache:/home/spotify/spotify \
        --name spotify \
        jess/spotify   
}
