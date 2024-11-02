import subprocess
import threading
import time
import requests
import socket

class NgrokSimulator:
    def __init__(self, ngrok_path="ngrok.exe", auth_token=None):
        """
        Initialize the NgrokSimulator with the path to ngrok executable and optional auth token.

        Args:
        ngrok_path (str): Path to the ngrok executable (default is 'ngrok.exe').
        auth_token (str): Optional ngrok authentication token.
        """
        self.ngrok_path = ngrok_path
        self.auth_token = auth_token
        self.process = None
        self.tunnel_thread = None
        self.public_url = None

        # Set up authentication if provided
        if self.auth_token:
            self.set_auth_token(self.auth_token)

    def set_auth_token(self, auth_token):
        """
        Set ngrok authentication token.

        Args:
        auth_token (str): Your ngrok authentication token.
        """
        command = [self.ngrok_path, "config", "add-authtoken", auth_token]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Ngrok authentication token set: {auth_token}")

    def start_tunnel(self, port=80):
        """
        Start an ngrok tunnel on the specified local port in a background thread.

        Args:
        port (int): Local port to expose via ngrok (default is 80).

        Returns:
        str: The public URL of the started tunnel.
        """
        # Check if localhost:4040 is already occupied and kill the process if needed
        self.free_port_4040()

        # Run the ngrok tunnel in a separate thread
        self.tunnel_thread = threading.Thread(target=self._run_ngrok, args=(port,))
        self.tunnel_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
        self.tunnel_thread.start()

        # Wait for the ngrok tunnel to initialize
        time.sleep(3)

        # Fetch the public URL from the ngrok API
        self.public_url = self.get_public_url()
        return self.public_url

    def _run_ngrok(self, port):
        """
        Private method to run ngrok and keep it alive in a background thread.

        Args:
        port (int): Local port to expose via ngrok.

        Returns:
        None
        """
        command = [self.ngrok_path, "http", str(port)]
        print(f"Starting ngrok with command: {' '.join(command)}")

        # Start ngrok process and capture its output
        self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get_public_url(self):
        """
        Retrieve the public URL of the running ngrok tunnel using the ngrok API.

        Returns:
        str: The public URL of the ngrok tunnel if found, else None.
        """
        try:
            response = requests.get("http://127.0.0.1:4040/api/tunnels")
            if response.status_code == 200:
                tunnels = response.json().get("tunnels", [])
                for tunnel in tunnels:
                    if tunnel.get("public_url"):
                        return tunnel["public_url"]
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving ngrok public URL: {e}")
        return None

    def free_port_4040(self):
        """
        Check if localhost:4040 is occupied and kill the process using it.

        Returns:
        None
        """
        # Check if port 4040 is open
        if self.is_port_in_use(4040):
            print("Port 4040 is in use. Attempting to free the port...")

            # Find and kill the process using port 4040
            pid = self.get_pid_using_port(4040)
            if pid:
                print(f"Killing process with PID: {pid} on port 4040...")
                self.kill_process_by_pid(pid)
                time.sleep(2)  # Wait a moment to ensure the port is freed
            else:
                print("No process found using port 4040.")

    def is_port_in_use(self, port):
        """
        Check if a specific port is in use on localhost.

        Args:
        port (int): The port number to check.

        Returns:
        bool: True if the port is in use, False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def get_pid_using_port(self, port):
        """
        Get the PID of the process using the specified port.

        Args:
        port (int): The port number to check.

        Returns:
        int: The PID of the process using the port, or None if not found.
        """
        result = subprocess.run(["netstat", "-aon", "|", "findstr", f":{port}"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            # Parse the output to find the PID
            lines = result.stdout.splitlines()
            for line in lines:
                if f":{port}" in line:
                    return int(line.split()[-1])  # The last column is the PID
        return None

    def kill_process_by_pid(self, pid):
        """
        Kill a process by its PID.

        Args:
        pid (int): The PID of the process to kill.

        Returns:
        None
        """
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
        print(f"Process {pid} has been terminated.")

    def stop_tunnel(self):
        """
        Stop the ngrok tunnel if it is running.
        """
        if self.process:
            self.process.terminate()
            print("Ngrok tunnel stopped.")
            self.process = None

    def wait_for_tunnel(self):
        """
        Keep the program running until the user manually stops it or interrupts.
        """
        try:
            print("Ngrok is running. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping ngrok tunnel...")
            self.stop_tunnel()

