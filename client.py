import grpc
import random
import game_pb2
import game_pb2_grpc
import datetime
import time
import Berkeley.berkeley_utils as brkl
class Client():

    def __init__(self) -> None:
        self.serverip = "localhost"  # input("paste ip here:")
        self.reg_name = input("put your name here:")
        self.first_port = 50051
        self.channel= grpc.insecure_channel(f"{self.serverip}:{self.first_port}")
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)
        self.reg_timestamp = str(datetime.datetime.now())
        self.total_processes = 3
        self.clients = set()

    def access_to_server(self):
    
        # with grpc.insecure_channel(f"{serverip}:{first_port}") as channel:
        #     stub = game_pb2_grpc.PlayerServiceStub(channel)
            request = game_pb2.AccessRequest()
            request.name = self.reg_name
            response = self.stub1.access_to_server(request)
            self.reg_symbol = response.symbol
            print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
            return response
    def set_symbol(self):
            request = game_pb2.PlayerRequest()
            request.position = self.reg_position
            request.symbol = self.reg_symbol
            request.timestamp = self.reg_timestamp
            self.stub2.start_game(request)

    def broadcastMessage(self):
        msg = game_pb2.MessageRequest(message = "hi")
        response_iterator = self.stub2.BroadcastMessage(msg)
        for response in response_iterator:
            print(response.message)

# broadcasting example
    def SendMessage(self, request_iterator, context):
        msg = game_pb2.MessageRequest(message = "hey")
        for client in self.clients:
            yield game_pb2.MessageResponse(msg.format(client))
            # yield hello_pb2.HelloReply(message="Server: Hello, {}!".format(client))

        for request in request_iterator:
            yield game_pb2.MessageResponse(msg.format(request.name))
                # yield hello_pb2.HelloReply(message="Server: Hello, {}!".format(request.name))  

# broadcasting example
    def Register(self, request, context):
        self.clients.add(request.name)
        print("Client {} registered".format(request.name))
        return game_pb2.Empty() 

    # first_port = 50051

if __name__ == "__main__": 
        a = Client()
        a.access_to_server()

        start_time = time.time()
        while (time.time() - start_time) < 3600:  # run for 1 hour (3600 seconds)
            
            time.sleep(1)  # add a delay to reduce CPU usage 