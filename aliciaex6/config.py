import grpc
import alicia_pb2
import alicia_pb2_grpc

total_processes = 4

first_port = 50051
last_port = first_port + total_processes -1
nodes_addresses = [first_port + i for i in range(total_processes)]

# Increase the maximum metadata size
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50 MB
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB
]
