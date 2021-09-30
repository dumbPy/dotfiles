
# Create my user in docker and transfer the ownership to me
changeowner(){
    IMAGE=$(docker images --format "{{.Repository}}:{{.Tag}}" | head -n 1)
    # if no docker image exists, use alpine:latest
    [[ $IMAGE ]] || IMAGE="alpine:latest"
    docker run -it -v $1:/mountpoint/app $IMAGE bash -c "addgroup $USER --gid $GID && useradd $USER -g $GID -u $UID && chown -R $USER:$USER /mountpoint/app"
}

ffprobe_get_time(){
    ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $1
}


# In TMUX sessions, forwarded ssh keys are not accessible. this fixes that issue
fixssh() {
eval $(tmux show-env -s |grep '^SSH_')
}
