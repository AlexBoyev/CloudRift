from backend_api.Docker.Docker import DockerManager

def init_docker():
    docker = DockerManager(r'C:\Users\Alex\PycharmProjects\CloudRift\backend_api\docker-compose.yaml')
    docker.build()
    docker.up()

init_docker()