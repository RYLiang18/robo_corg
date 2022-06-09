# !/bin/zsh
heroku container:login

heroku container:push worker -a robo-corg
heroku container:release worker -a robo-corg