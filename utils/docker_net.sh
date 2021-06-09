#put all the docker hosts in a docker sworm. Once the docker swarm is created run:

docker network create --driver=overlay --subnet=10.0.0.0/16 --ip-range 10.0.1.0/24 --gateway 10.0.0.1 --attachable test-net
