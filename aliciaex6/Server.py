#to run using python Server.py
from concurrent import futures
import numpy as np
from queue import Queue
import time
from config import *
import berkeley_utils as brkl
import datetime
import grpc
import alicia_pb2
import alicia_pb2_grpc

class EditDistanceServiceServicer(alicia_pb2_grpc.EditDistanceServiceServicer):
    def __init__(self, process_id):
        self.process_id = process_id

    def EditDistance(self, request, context):
        if request.leader != self.process_id:
            return alicia_pb2.EditDistanceResponse(distance=-1)

        first_word = request.first_word
        second_word = request.second_word
        distance = self.EditDistanceGranted(first_word, second_word)

        return alicia_pb2.EditDistanceResponse(distance=distance)

    def EditDistanceGranted(self, s1, s2):
        a_table = np.zeros((len(s1) + 1, len(s2) + 1), dtype=int)

        for i in range(len(s1) + 1):
            a_table[i][0] = i

        for i in range(len(s2) + 1):
            a_table[0][i] = i

        for i1 in range(1, len(s1) + 1):
            for i2 in range(1, len(s2) + 1):
                if s1[i1 - 1] == s2[i2 - 1]:
                    a_table[i1][i2] = a_table[i1 - 1][i2 - 1]
                else:
                    delete = a_table[i1 - 1][i2]
                    insert = a_table[i1][i2 - 1]
                    substitute = a_table[i1 - 1][i2 - 1]
                    transpose = a_table[i1 - 2][i2 - 2] if i1 > 1 and i2 > 1 and s1[i1 - 1] == s2[i2 - 2] and s1[i1 - 2] == s2[i2 - 1] else float('inf')

                    a_table[i1][i2] = 1 + min(delete, insert, substitute, transpose)

        dist = a_table[len(s1)][len(s2)]
        return dist

    
class RingElectionServicer(alicia_pb2_grpc.RingElectionServicer):
    def __init__(self, id):
        self.id = int(id)

    def set_next_node(self, next_node_address):
        self.next_node_address = int(next_node_address)

    def StartElection(self, request, context):
        brkl.print_with_berkeley_time(f"Node {self.id} received message: {request}")
        message = alicia_pb2.Message()
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
            #this won't work if max port is down.
            #also we should create cache to store the queue of nodes.
            return message
        

        while True:
            try:
                with grpc.insecure_channel(f"localhost:{self.next_node_address}") as channel:
                    stub = alicia_pb2_grpc.RingElectionStub(channel)
                    response = stub.StartElection(message)
                    return response
            except grpc.RpcError as e:
                brkl.print_with_berkeley_time(f"Node {self.next_node_address} is down. We run localhost:{self.next_node_address+1} instead.")
                self.next_node_address += 1
                
                if self.next_node_address  > first_port + total_processes - 1:
                    self.next_node_address  = first_port
                if self.next_node_address  == self.id:
                    print("All nodes seem to be down. Exiting.")
                    return

class BerkeleySynchronizationServicer(alicia_pb2_grpc.BerkeleySynchronizationServicer):
    def __init__(self):
        self.current_time = time.time()

    def RequestTime(self, request, context):
        current_time = time.time()
        return alicia_pb2.TimeResponse(time=int(current_time))

    def AdjustTime(self, request, context):
        self.current_time += request.adjustment
        return alicia_pb2.Empty()
    

def serve(id, address, next_node_address):
    time_synchronization_servicer = BerkeleySynchronizationServicer()
    edit_distance_servicer = EditDistanceServiceServicer(id)
    ring_election_servicer = RingElectionServicer(id)
    ring_election_servicer.set_next_node(next_node_address)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5), options=options)
    alicia_pb2_grpc.add_BerkeleySynchronizationServicer_to_server(time_synchronization_servicer, server)
    alicia_pb2_grpc.add_EditDistanceServiceServicer_to_server(edit_distance_servicer, server)
    alicia_pb2_grpc.add_RingElectionServicer_to_server(ring_election_servicer, server)
    
    server.add_insecure_port(f"localhost:{address}")

    server.start()

    print(f"Node {id} started at {address}. Its next node is {next_node_address}")
    server.wait_for_termination()

if __name__ == "__main__":
    port1 = input("Please put your port id:")
    port2 = int(port1) + 1 if int(port1) < first_port + total_processes - 1 else first_port

    address = int(port1)
    next_node_address = int(port2)
    serve(address, address, next_node_address)