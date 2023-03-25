import grpc
import game_pb2
import game_pb2_grpc
import socket

your_selected_port = 50051
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")
nicknames = ["SiamSavage","PangPapaya","TheTeaThief","GanjaGandalf","BakuBrawler","KababKing","SabaSaber","ChaiChaos","GazelleGigolo","ThaiTsunami"]

time_limit = 60
total_processes = 3
ip = "172.80.0.1"
first_port = 50051
last_port = first_port + total_processes -1
nodes_addresses = [first_port + i for i in range(total_processes)]

# Increase the maximum metadata size
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50 MB
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB
]