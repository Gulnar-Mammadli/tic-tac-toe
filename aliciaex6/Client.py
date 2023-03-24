#to run using python Client.py

import random
import berkeley_utils as brkl
from config import *

def run_ring_election(nodes_addresses):
    origin = 50051#random.randint(first_port, first_port + total_processes - 1)
    initial_message = alicia_pb2.Message(
        origin=origin, max_id=origin, rounds=0, leader=-1)
    brkl.print_with_berkeley_time(f"Starting election from node {origin}")
    try:
        with grpc.insecure_channel(f"localhost:{nodes_addresses[origin-first_port]}") as channel:
            stub = alicia_pb2_grpc.RingElectionStub(channel)
            response = stub.StartElection(initial_message)
    except grpc.RpcError as e:
        print(f"Node {nodes_addresses[origin-first_port]} is down. Trying another node.")
        return None

    brkl.print_with_berkeley_time(f"The elected leader is Node {response.leader}")
    return response.leader

def run_edit_distance(leader, first_word, second_word):
    if leader is None:
        print("Cannot calculate edit distance without a leader.")
        return

    request = alicia_pb2.EditDistanceRequest(process_id=leader, leader=leader, first_word=first_word, second_word=second_word)
    
    try:
        with grpc.insecure_channel(f"localhost:{leader}") as channel:
            stub = alicia_pb2_grpc.EditDistanceServiceStub(channel)
            response = stub.EditDistance(request)
            brkl.print_with_berkeley_time(f"'{first_word}' and '{second_word}': {response.distance}")
    except grpc.RpcError as e:
        print(f"{leader} is down. run client again to reselect the node")







if __name__ == "__main__":
    leader = run_ring_election(nodes_addresses)
    brkl.synchronize_time(nodes_addresses)

    run_edit_distance(leader, "moomin", "miimu")