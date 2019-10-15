kaggle(){
    sudo docker run -it --rm \
    -v /home/sufiyan/kaggle:/root/kaggle \
    -v /home/sufiyan/kaggle/.kaggle:/root/.kaggle \
    sufiyan/kaggle
}
