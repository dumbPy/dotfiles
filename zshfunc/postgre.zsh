
postgre_without_topology(){
    docker run -d --name postgre_without_topology -p 5431:5432 -e FILE=WITHOUT registry.curlhg.io/vakt/vakt:psql_with_without
    echo "running on port 5431"
}

postgre_with_topology(){
    docker run -d --name postgre_with_topology -p 5432:5432 -e FILE=WITH registry.curlhg.io/vakt/vakt:psql_with_without
    echo "running on port 5432"
}
