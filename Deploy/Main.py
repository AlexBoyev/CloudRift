import time

from backend_api.Docker.Docker import DockerManager
from backend_api.Ngrok.Ngrok import NgrokSimulator


def init_docker():
    docker = DockerManager(r'C:\Users\Alex\PycharmProjects\CloudRift\backend_api\docker-compose.yaml')
    docker.build()
    docker.up()

def init_ngrok():
    manager = NgrokSimulator(ngrok_path=r'C:\Users\Alex\Desktop\ngrok.exe',
                             auth_token="2mCrZKgvrphEth69z5S45ijbxfQ_79W64uknaCwmjXpgd99qq")
    public_url = manager.start_tunnel()
    print((public_url))
    time.sleep(18000)
    manager.stop_tunnel()


init_docker()
init_ngrok()