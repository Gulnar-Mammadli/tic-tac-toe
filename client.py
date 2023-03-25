from time import sleep
import grpc
import game_pb2
import game_pb2_grpc
import datetime
from config import *
from tutorial import *
import time 

import Ring.ring_utils as rng
import Berkeley.berkeley_utils as brkl
import time 
import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux, macOS)
        os.system('clear')
        
class Client():

    def __init__(self) -> None:
        self.serverip = "localhost"  # input("paste ip here:")
        self.reg_name = "alicia"#input("put your name here:")
        self.port = input("put your port here:")
        self.set_stub()
        self.reg_timestamp = str(datetime.datetime.now())
        self.id = ""
        self.leader = 0
        self.found_winner = False
        self.tie = False

    def set_stub(self):
        self.channel= grpc.insecure_channel(f'{self.serverip}:{self.port}')
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)
        self.ringstub = rng.Ring.ring_pb2_grpc.RingElectionStub(self.channel)


    def leader_message(self):
        while(True):
            ans = input("Type ring command to start leader election: ")
            if ans=="ring":
                self.leader = run_ring_election()
                print(self.leader)
            else:
                request = game_pb2.MessageRequest(message = str(last_port))
                response = self.stub1.leader_message(request)
                self.leader = int(response.message)
                if self.leader != last_port:
                    print(f"{self.leader} : {last_port}")
                    print("leader not found. wait a bit until the election is finished.")
                elif self.port == self.leader:
                    print("you are the game master") #TODO game master cmd
                else:
                    break
        
        list_tutorial() 

    def connect_to_leader(self):  
        self.port = self.leader
        self.set_stub()
        self.access_to_server()

    def access_to_server(self):
        request = game_pb2.AccessRequest()
        request.name = self.reg_name
        response = self.stub1.access_to_server(request)
        self.id = response.id
        self.reg_symbol = response.symbol
        print(f"your id: {response.id} symbol {response.symbol}")  
        print(f"{response.game_status}")
        self.is_your_turn = False
        return response
    
    def logout(self):
        req = game_pb2.MessageRequest(message=self.id)
        response = self.stub1.logout(req)
        print(response.message)
        return response
    
    def list_board(self):
        print("Here is current board:")
        request = game_pb2.GameEmpty()
        response = self.stub2.list_board(request)
        print(f"{response.message}")
         
    def set_symbol(self, pos, diff):
        request = game_pb2.PlayerRequest()
        request.position = int(pos[0])
        request.symbol = self.reg_symbol
        request.timestamp = str(diff)
        response = self.stub1.set_symbol(request)
        self.found_winner = response.victory
        print(response.symbol)
        print(response.position)
        print(response.game_board)
        self.tie = response.symbol =="TIE!!"

    def check_status(self):
        request = game_pb2.GameEmpty()
        response = self.stub1.check_status(request)
        print(response.message)

    def check_winner(self):
        if self.found_winner == True:
            print(f"{self.found_winner} found winner")
            
        return self.found_winner

    def restart(self):
        self.found_winner = False
        request = game_pb2.AccessRequest(name = self.id)
        response = self.stub1.restart(request)
        print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
        print(f"{response.game_status}")

    def sync_time(self):
        print("berkeley")

    def start_game(self):
        global clear_screen
        commands = {
        "ring": run_ring_election,
        "berkeley": self.sync_time ,
        "board": self.list_board,
        "status": lambda: self.check_status,
        "": lambda: self.list_board,
        "countdown": lambda: print("countdown time:"),
        }

        while(True):

            if (self.check_winner()):
                break

            start = time.time()    
            cmd = input("Type your command: ")
            end = time.time()
            difference = end - start
            decision_time = int(difference)
            if decision_time > time_limit:
                print("You took lots of time to decide.You lost your turn")

            if cmd == "quit":
                self.logout()
                sleep(1)
                break
            elif len(cmd) > 0 and cmd[0].isdigit():
                if (self.check_winner()):
                    break
                self.set_symbol(cmd, decision_time)
            else:
                action = commands.get(cmd, lambda: print("No command found"))
                action()

        restart = input("Do want to play Again?(y/n)")

        if restart == "y" or restart == "Y": 
            restartstr = input("please type ready to start the game:")
            if restartstr.lower() == "ready":
                self.restart()
                self.get_cmd()

        self.logout()

a = Client()
    
def run_ring_election():
    origin = 50051
    initial_message = rng.Ring.ring_pb2.RingMessage(
        origin=origin, max_id=origin, rounds=0, leader=-1)
    #brkl.print_with_berkeley_time(f"Starting election from node {origin}")
    #try:

    response = a.ringstub.StartElection(initial_message)
    # except grpc.RpcError as e:
    #     print(f"Node {nodes_addresses[origin-first_port]} is down. Trying another node.")
    #     return None

    #brkl.print_with_berkeley_time(f"The elected leader is Node {response.leader}")
    return response.leader


if __name__ == "__main__": 
    a.access_to_server()
    list_tutorial()
    try:
        a.leader_message()
        a.connect_to_leader()
        a.list_board()
        list_game_cmd()
        a.start_game()
    except KeyboardInterrupt:
        print("you quit the game.")
        a.logout()
        sleep(1)


