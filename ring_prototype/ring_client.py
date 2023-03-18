import grpc
import random
import ring_pb2
import ring_pb2_grpc


def run_ring_algorithm():
    origin = random.randint(first_port, first_port + total_processes - 1)
    initial_message = ring_pb2.Message(
        origin=origin, max_id=origin, rounds=0, leader=-1)
    print(f"Starting from node {origin}")

    try:
        with grpc.insecure_channel(f"localhost:{nodes_addresses[origin-first_port]}") as channel:
            stub = ring_pb2_grpc.RingStub(channel)
            response = stub.PassMessage(initial_message)
    except grpc.RpcError as e:
        print(f"Node {nodes_addresses[origin-first_port]} is down. Trying another node.")

    print(f"The elected leader is Node {response.leader}")


total_processes = 6
first_port = 50051
nodes_addresses = [50051, 50052,  50053, 50054, 50055, 50056]

if __name__ == "__main__":
    run_ring_algorithm()
