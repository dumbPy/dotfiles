spacemacs_docker(){
docker run -ti --name spacemacs \
    -e DISPLAY="unix$DISPLAY" \
    -e UNAME="sufiyan" \
    -e UID="$UID" \
    -e TZ="Asia/Kolkata" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/machine-id:/etc/machine-id:ro \
    -v /var/run/dbus:/var/run/dbus \
    -v /home/sufiyan/curl/sara-backend:/mnt/workspace \
    spacemacs/develop
}
