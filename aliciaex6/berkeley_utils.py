import datetime
import grpc
import alicia_pb2
import alicia_pb2_grpc
from config import *
from grpc import ChannelConnectivity
import time

#ALL METHODS CAN BE USE IF AND ONLY IF ALL PORTS ARE RUNNING

def synchronize_time(nodes_addresses):
    times = []
    for address in nodes_addresses:
        node_time = request_time_from_node(address)
        if node_time is not None:
            times.append(node_time)

    if len(times) == 0:
        print("No available nodes to synchronize time.")
        return None

    average_time = sum(times) / len(times)
    print(f"Average time: {average_time}")

    for address in nodes_addresses:
        node_time = request_time_from_node(address)
        if node_time is not None:
            adjustment = average_time - node_time
            print(f"Adjusting time of Node {address} by {adjustment} seconds")
            adjust_time_of_node(address, adjustment)

    return average_time


def request_time_from_node(node_address):
    try:
        with grpc.insecure_channel(f"localhost:{node_address}") as channel:
            stub = alicia_pb2_grpc.BerkeleySynchronizationStub(channel)
            response = stub.RequestTime(alicia_pb2.Empty())
            node_time = response.time
            local_time = time.time()
            time_difference = node_time - local_time
            return time_difference
    except grpc.RpcError as e:
        print(f"Failed to request time from Node {node_address}. Error: {e}")
        return None


def adjust_time_of_node(node_address, adjustment):
    try:
        with grpc.insecure_channel(f"localhost:{node_address}") as channel:
            stub = alicia_pb2_grpc.BerkeleySynchronizationStub(channel)
            request = alicia_pb2.TimeAdjustment(adjustment=int(adjustment))
            stub.AdjustTime(request)
    except grpc.RpcError as e:
        print(f"Failed to adjust time of Node {node_address}. Error: {e}")

def print_with_berkeley_time(message):
    average_time = synchronize_time(nodes_addresses)

    if average_time is not None:
        berkeley_time = datetime.datetime.now() + datetime.timedelta(seconds=average_time)
    else:
        print("Cannot calculate Berkeley time due to no available nodes.")

    berkeley_time = datetime.datetime.now() + datetime.timedelta(seconds=average_time)
    print(f"{message} at {berkeley_time}")



