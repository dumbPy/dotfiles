kaggle(){
    sudo docker run -it --rm \
    -v /home/sufiyan/kaggle:/root/kaggle \
    -v /home/sufiyan/kaggle/.kaggle:/root/.kaggle \
    sufiyan/kaggle
}

docker_emacs() {
sudo docker run -ti --name spacemacs \
 -e DISPLAY="unix$DISPLAY" \
 -e UNAME="spacemacser" \
 -e UID="1000" \
 -e TZ="Asia/Kolkata" \
 -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
 -v /etc/localtime:/etc/localtime:ro \
 -v /etc/machine-id:/etc/machine-id:ro \
 -v /var/run/dbus:/var/run/dbus \
 -v "/home/sufiyan/Downloads/template/temp_1_lw":/mnt/workspace \
 spacemacs/develop
}
