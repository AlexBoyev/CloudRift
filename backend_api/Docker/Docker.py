import subprocess


class DockerManager:
    def __init__(self, compose_file='docker-compose.yml'):
        """
        Initialize the DockerManager with a specific docker-compose file.

        Args:
        compose_file (str): Path to the docker-compose file.
        """
        self.compose_file = compose_file

    def build(self, service=None):
        """
        Run 'docker-compose build'.

        Args:
        service (str): Specific service to build (optional).
        """
        command = ['docker-compose', '-f', self.compose_file, 'build']
        if service:
            command.append(service)
        self._run_command(command)

    def up(self, service=None, detach=True):
        """
        Run 'docker-compose up'.

        Args:
        service (str): Specific service to start (optional).
        detach (bool): Run in detached mode if True (adds the '-d' flag).
        """
        command = ['docker-compose', '-f', self.compose_file, 'up']
        if detach:
            command.append('-d')
        if service:
            command.append(service)
        self._run_command(command)

    def down(self, remove_volumes=False):
        """
        Run 'docker-compose down'.

        Args:
        remove_volumes (bool): Remove named volumes if True.
        """
        command = ['docker-compose', '-f', self.compose_file, 'down']
        if remove_volumes:
            command.append('-v')
        self._run_command(command)

    def delete(self, service=None, remove_volumes=False):
        """
        Run 'docker-compose rm' to delete containers.

        Args:
        service (str): Specific service to delete (optional).
        remove_volumes (bool): Remove volumes associated with the service.
        """
        command = ['docker-compose', '-f', self.compose_file, 'rm', '-f']
        if remove_volumes:
            command.append('-v')
        if service:
            command.append(service)
        self._run_command(command)

    def _run_command(self, command):
        """
        Run a system command using subprocess.

        Args:
        command (list): Command and arguments to execute.
        """
        print(f"Executing command: {' '.join(command)}")
        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e.stderr.decode('utf-8')}")

