import grpc
import random
import game_pb2
import game_pb2_grpc

def access_to_server():
    serverip = "localhost"  # input("paste ip here:")
    reg_name = input("put your name here:")


    with grpc.insecure_channel(f"{serverip}:{first_port}") as channel:
        stub = game_pb2_grpc.PlayerServiceStub(channel)
        request = game_pb2.AccessRequest()
        request.name = reg_name
        response = stub.access_to_server(request)
        print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
        return response

total_processes = 3
first_port = 50051

if __name__ == "__main__":
    access_to_server()