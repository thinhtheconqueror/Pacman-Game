"""
network.py

Handles client-server communication using sockets and pickle for object serialization.
"""
import socket
import pickle
import struct

def send_msg(sock, msg_data):
    """Serialize and send data with a 4-byte length prefix."""
    serialized = pickle.dumps(msg_data)
    length_prefix = struct.pack('>I', len(serialized))
    sock.sendall(length_prefix + serialized)

def recv_msg(sock):
    """Receive a length-prefixed message and deserialize it."""
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    serialized = recvall(sock, msglen)
    if not serialized:
        return None
    return pickle.loads(serialized)

def recvall(sock, n):
    """Helper function to recv n bytes or return None if EOF is hit."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

class Network:
    """Manages the network connection for a multiplayer client."""
    def __init__(self, host="127.0.0.1", port=5555):
        """Initializes the network client and establishes connection."""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = host
        self.port = port
        self.addr = (self.server, self.port)
        self.p_id = self.connect()
        self.role_info = None  # Will store role assignment from server

    def connect(self):
        """Attempts to connect to the server and retrieves a player ID."""
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
            send_msg(self.client, {"type": "init", "role": role})
            # Receive role assignment response
            response = recv_msg(self.client)
            self.role_info = response
            return response
        except socket.error as e:
            print(e)
            return None

    def send(self, data):
        """Sends data (keystrokes/commands) and receives game state."""
        try:
            send_msg(self.client, data)
            return recv_msg(self.client)
        except socket.error as e:
            print(e)
            return None
