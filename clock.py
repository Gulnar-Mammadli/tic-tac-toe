import time
import socket

class Node:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clock = time.time()
        self.offset = 0

    def set_time(self, new_time):
        self.offset = new_time - time.time()

    def get_time(self):
        return time.time() + self.offset

    def sync_time(self, master):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((master.ip, master.port))
        s.sendall(str(self.clock).encode())
        data = s.recv(1024)
        s.close()
        new_time = float(data.decode())
        self.set_time(new_time)

    def run(self, master):
        while True:
            self.sync_time(master)
            time.sleep(1)

class Master:
    def __init__(self, nodes):
        self.nodes = nodes

    def run(self):
        while True:
            timestamps = []
            for node in self.nodes:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((node.ip, node.port))
                s.listen(1)
                conn, addr = s.accept()
                data = conn.recv(1024)
                conn.close()
                timestamp = float(data.decode())
                timestamps.append(timestamp)
            avg_timestamp = sum(timestamps) / len(timestamps)
            for node in self.nodes:
                node.set_time(avg_timestamp)
            time.sleep(1)

if __name__ == '__main__':
    node1 = Node('localhost', 8000)
    node2 = Node('localhost', 8001)
    node3 = Node('localhost', 8002)
    nodes = [node1, node2, node3]
    master = Master(nodes)
    node1.run(master)
