# relies on math.sh for calc and f2i functions


st_generate_epf(){
    # rates
    # local rate_basic=390.77 # basic rate per day
    # local rate_ot=97.69 # ot charges per hour
    local rate_basic=404.23 # basic rate per day
    local rate_ot=101.06 # ot charges per hour


    local days=$1
    local ot=$2

    local ncp_days=$(calc "26 - $days")


    local basic_n_hra=$(calc "$days*$rate_basic*1.05")
    echo $basic_n_hra
    local net_ot=$(calc "$rate_ot*$ot")

    echo "100787538471#~#SANGANNA MALLAPA MAINAL#~#\
$(f2i $(calc "$basic_n_hra+$net_ot"))#~#\
$(f2i $basic_n_hra)#~#$(f2i $basic_n_hra)#~#$(f2i $basic_n_hra)#~#\
$(f2i $(calc "$basic_n_hra*0.12"))#~#\
$(f2i $(calc "$basic_n_hra*0.0833"))\
#~#$(f2i $(calc "$basic_n_hra*0.0367"))#~#\
$ncp_days#~#0" > EPFO_$(date --date="$(date +%Y-%m-15) - 1 month" +%b_%y).txt
}
