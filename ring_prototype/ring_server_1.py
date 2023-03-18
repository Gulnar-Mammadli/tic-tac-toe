import grpc
from concurrent import futures

import game_pb2
import game_pb2_grpc

# Increase the maximum metadata size
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50 MB
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB
]


class Node(game_pb2_grpc.AdminServiceServicer):
    def __init__(self, id):
        self.id = int(id)

    def set_next_node(self, next_node_address):
        self.next_node_address = int(next_node_address)

    def PassMessage(self, request, context):
        print(f"Node {self.id} received message: {request}")
        message = game_pb2.Message()
        message.origin = request.origin
        message.rounds = request.rounds
        message.max_id = max(request.max_id, self.id)
        print(message.max_id)

        if request.origin == self.id and request.rounds == 1:
            message.leader = message.max_id
            return message
        else:
            message.leader = message.max_id if message.max_id == self.id else -1

        if message.max_id == first_port + total_processes - 1: 
            #this won't work if 50056 is down.
            #also we should create cache to store the queue of nodes.
            return message
        

        while True:
            try:
                with grpc.insecure_channel(f"localhost:{self.next_node_address}") as channel:
                    stub = game_pb2_grpc.AdminServiceStub(channel)
                    response = stub.PassMessage(message)
                    return response
            except grpc.RpcError as e:
                print(f"Node {self.next_node_address} is down. We run localhost:{self.next_node_address+1} instead.")
                self.next_node_address += 1
                
                if self.next_node_address  > first_port + total_processes - 1:
                    self.next_node_address  = first_port
                if self.next_node_address  == self.id:
                    print("All nodes seem to be down. Exiting.")
                    return
        

def serve(id, address, next_node_address):
    node = Node(id)
    node.set_next_node(next_node_address)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    game_pb2_grpc.add_AdminServiceServicer_to_server(node, server)
    server.add_insecure_port(f"localhost:{port1}")
    server.start()
    print(f"Node {id} started at {address}. Its next node is {port2}")
    server.wait_for_termination()


total_processes = 6
first_port = 50051

if __name__ == "__main__":
    # Configure the node IDs, addresses, and next_node_addresses
    port1 = input("please put your port id:")
    port2 = int(port1)+1 if int(port1) < first_port + total_processes - 1 else first_port


    address = int(port1)
    next_node_address = int(port2)
    serve(address,address, next_node_address)
