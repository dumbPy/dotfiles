
# Create my user in docker and transfer the ownership to me
changeowner(){
    IMAGE=$(docker images --format "{{.Repository}}:{{.Tag}}" | head -n 1)
    # if no docker image exists, use alpine:latest
    [[ $IMAGE ]] || IMAGE="alpine:latest"
    docker run -it -v $1:/mountpoint/app $IMAGE bash -c "addgroup $USER --gid $GID && useradd $USER -g $GID -u $UID && chown -R $USER:$USER /mountpoint/app"
}