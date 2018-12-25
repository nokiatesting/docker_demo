# docker_demo
A python web application on docker for demo

commands:
docker build -t demo_img .

docker history demo_img

docker run -d --name demo -P demo_img

docker logs demo
