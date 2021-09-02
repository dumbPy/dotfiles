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
    -v /home/sufiyan/workspace/tasks:/mnt/workspace \
    spacemacs/develop
}

# list compose projects running
composelist(){
    docker ps --filter "label=com.docker.compose.project" -q | xargs docker inspect --format='{{index .Config.Labels "com.docker.compose.project"}}'| sort | uniq
}