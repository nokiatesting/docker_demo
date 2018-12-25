# docker_demo
A python web application on docker for demo

commands:

docker run -d -e MYSQL_ROOT_PASSWORD=root -v mydata:/var/lib/mysql --name mysql mysql:5

docker network create testnet

docker network connect testnet mysql

create database testdb

docker run -d --name demo2 -P --network=testnet nokiatesting/docker_demo:mysql
