
f2i(){
    echo "$(printf "%.0f\n" $1)"
    }

calc(){
    echo $(echo $1 | bc)
}
