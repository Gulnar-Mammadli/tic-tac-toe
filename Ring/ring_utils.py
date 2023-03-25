import grpc
import Ring.ring_pb2
import Ring.ring_pb2_grpc
from config import *
from Berkeley import berkeley_utils as brkl

class RingElectionServicer(Ring.ring_pb2_grpc.RingElectionServicer):
    def __init__(self, id):
        self.id = int(id)
        self.leader_port = int(id)
    def set_next_node(self, next_node_address):
        self.next_node_address = int(next_node_address)

    def StartElection(self, request, context):
        brkl.print_with_berkeley_time(f"Node {self.id} received message: {request}")
        message = Ring.ring_pb2.RingMessage()
        message.origin = request.origin
        message.rounds = request.rounds
        message.max_id = max(request.max_id, self.id)
        brkl.print_with_berkeley_time(message.max_id)

        if request.origin == self.id and request.rounds == 1:
            message.leader = message.max_id
            return message
        else:
            message.leader = message.max_id if message.max_id == self.id else -1

        if message.max_id == first_port + total_processes - 1: 
            self.leader_port = message.leader
            message.leader = message.max_id
            print(f"leader found {message.leader}")
            return message

        while True:
            try:
                with grpc.insecure_channel(f"localhost:{self.next_node_address}") as channel:
                    stub = Ring.ring_pb2_grpc.RingElectionStub(channel)
                    response = stub.StartElection(message)
                    self.leader_port = response.leader #response only at 50051-50052 
                    return response
            except grpc.RpcError as e:
                brkl.print_with_berkeley_time(f"Node {self.next_node_address} is down. We run localhost:{self.next_node_address+1} instead.")
                self.next_node_address += 1
                
                if self.next_node_address  > first_port + total_processes - 1:
                    self.next_node_address  = first_port
                if self.next_node_address  == self.id:
                    print("All nodes seem to be down. Exiting.")
                    return