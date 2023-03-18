import grpc
import random
import game_pb2
import game_pb2_grpc

class Client():

    def __init__(self) -> None:
        self.serverip = "localhost"  # input("paste ip here:")
        self.reg_name = input("put your name here:")
        self.first_port = 50051
        self.channel= grpc.insecure_channel(f"{self.serverip}:{self.first_port}")
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)
        self.total_processes = 3
    def access_to_server(self):
    
        # with grpc.insecure_channel(f"{serverip}:{first_port}") as channel:
        #     stub = game_pb2_grpc.PlayerServiceStub(channel)
            request = game_pb2.AccessRequest()
            request.name = self.reg_name
            response = self.stub1.access_to_server(request)
            print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
            return response
    def start_game(self):
            request = game_pb2.PlayerRequest()
            self.stub2.start_game(request)
    # first_port = 50051

if __name__ == "__main__": 
        a = Client()
        a.access_to_server()
        a.start_game()    