import grpc
import game_pb2
import game_pb2_grpc
import datetime
from config import *

#import Berkeley.berkeley_utils as brkl
class Client():

    def __init__(self) -> None:
        self.serverip = "localhost"  # input("paste ip here:")
        self.reg_name = input("put your name here:")
        self.first_port = 50051
        self.channel= grpc.insecure_channel(f'{self.serverip}:{self.first_port}')
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)
        self.reg_timestamp = str(datetime.datetime.now())
        self.total_processes = 3
        #self.clients = set()

    def access_to_server(self):
        request = game_pb2.AccessRequest()
        request.name = self.reg_name
        response = self.stub1.access_to_server(request)
        self.reg_symbol = response.symbol
        print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
        print(f"{response.game_status}")
        return response
    
    def list_board(self):
        print("Here is current board:")
        request = game_pb2.GameEmpty()
        response = self.stub2.list_board(request)
        print(f"{response.message}")
         
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
    
def list_tutorial():
    print("How to play the game: ")
    print("1. you will be assigned the symbol from the game master.")
    print("2. once it is your turn, just give the position at range 1-9.")

def get_cmd():
    while(True):
        cmd = input("type your command to the game master: ")
        match cmd:
            case "board":
                a.list_board()
            case "status":
                print("You can become a web developer.")
            case "1":
                print("You can become a Data Scientist")
            case "2":
                print("You can become a backend developer")
            case "3":
                print("You can become a Blockchain developer")
            case "4":
                print("You can become a mobile app developer")
            case "5":
                print("You can become a mobile app developer")
            case "6":
                print("You can become a mobile app developer")
            case "7":
                print("You can become a mobile app developer")
            case "8":
                print("You can become a mobile app developer")
            case "9":
                print("You can become a mobile app developer")
            case _:
                print("no command found")

if __name__ == "__main__": 
    a = Client()
    a.access_to_server()
    a.list_board()
    list_tutorial()


