-Stop all running containers
docker stop $(docker ps -aq)

-Remove all containers
docker rm $(docker ps -aq)

-Remove all images
docker rmi $(docker images -q)

----Remove All unused Docker Objects
docker system prune -a --volumes
