import socket
import pickle

class Network:
    def __init__(self, host="127.0.0.1", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = host
        self.port = port
        self.addr = (self.server, self.port)
        self.p_id = self.connect()
        self.role_info = None  # Will store role assignment from server

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = self.client.recv(2048).decode()
            pid = int(data)
            if pid == -1:
                print("Server is full!")
                return None
            return pid
        except Exception as e:
            print("Connection error:", e)
            return None

    def send_init(self, role):
        """Send initial role request and receive role assignment."""
        try:
            self.client.send(pickle.dumps({"type": "init", "role": role}))
            # Receive role assignment response
            response = pickle.loads(self.client.recv(4096))
            self.role_info = response
            return response
        except socket.error as e:
            print(e)
            return None

    def send(self, data):
        """Sends data (keystrokes/commands) and receives game state."""
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(65536))
        except socket.error as e:
            print(e)
            return None
