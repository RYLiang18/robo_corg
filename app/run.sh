read -p 'CMD: ' usr_cmd

docker build -t giich_robocorg_image .
docker run \
    -it \
    --env-file .env \
    --name giich_robocorg_container \
    giich_robocorg_image:latest \
    $usr_cmd

docker container rm giich_robocorg_container
docker image rm giich_robocorg_image:latest