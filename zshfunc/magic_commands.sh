
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

rmff(){
    # Func to delete a file or a folder by mounting it to a docker
    # --------------------------------------------------------------
    # check if the file exists
    [[ ! -e $1 ]] && echo "usage: docker_mount_and_rm \<file or folder path\> [ --dry-run ]" && exit 1
    # get the first image. any image works for this task
    IMAGE=$(docker images --format "{{.Repository}}:{{.Tag}}" | head -n 1)
    # if no docker image exists, use alpine:latest
    [[ $IMAGE ]] || IMAGE="alpine:latest"
    if [[ $# -ge 2 ]]
    then
        case "$2" in
            --dry-run) # if second argument is --dry-run
                # print the command instead of running it
                echo "docker run --rm -v $(dirname $(readlink -f $1)):/workspace $IMAGE bash -c \"rm -rf /workspace/$(basename $(readlink -f $1))\""
                exit 0
                ;;
            # Else for any other second argument, print help and exit
            *)
                echo "usage: docker_mount_and_rm \<file or folder path\> [ --dry-run ]" && exit 1
        esac
    fi
    docker run --rm -v $(dirname $(readlink -f $1)):/workspace $IMAGE bash -c "rm -rf /workspace/$(basename $(readlink -f $1))"
}