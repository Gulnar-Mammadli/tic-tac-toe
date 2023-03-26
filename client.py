from time import sleep
import grpc
import game_pb2
import game_pb2_grpc
import datetime
from config import *
from tutorial import *
import time 
import random
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
        self.reg_name = random.choice(nicknames)#input("put your name here:")
        self.port = input("put your port here:")
        self.init_client_data()

    def init_client_data(self):
        self.serverip = ip(int(self.port))  # input("paste ip here:")
        self.set_stub()
        self.reg_timestamp = str(datetime.datetime.now())
        self.id = ""
        self.leader = 0
        self.found_winner = False
        self.tie = False

    def set_stub(self):
        self.channel= grpc.insecure_channel(f'{ip(self.serverip)}:{self.port}')
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
                elif self.port == str(self.leader):
                    print("you are the game master") #TODO game master cmd
                    list_ADMIN_cmd()
                    break
                elif self.port != str(self.leader):
                    self.connect_to_leader()
                    break
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
        if hasattr(response, 'position'):
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
        self.tie = False
        request = game_pb2.AccessRequest(name = self.id)
        print(self.id+" restart")
        response = self.stub1.restart(request)
        print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
        print(f"{response.game_status}")

    def start_game(self):
        global clear_screen
        commands = {
        "list-board": self.list_board,
        "status": lambda: self.check_status,
        "": lambda: self.list_board,
        "countdown": lambda: print("countdown time:"),
        }

        while not self.check_winner() and not self.tie:
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
                self.set_symbol(cmd, decision_time)

            else:
                action = commands.get(cmd, lambda: print("No command found"))
                action()

        restart = input("Do want to play Again?(y/n)")

        if restart == "y" or restart == "Y": 
            restartstr = input("please type start-game to start the game:")
            if restartstr.lower() == "start-game":
                self.restart()
                self.start_game()

        self.logout()

class Admin(Client):

    def __init__(self) -> None:
        self.reg_name = c.reg_name
        self.port =  c.port
        self.init_client_data()

    def init_client_data(self):
        self.serverip = "localhost"  # input("paste ip here:")
        self.set_stub(self.port)
        self.reg_timestamp = str(datetime.datetime.now())
        self.id = c.id 
        self.leader = c.leader
        self.found_winner = c.found_winner
        self.tie = c.tie

    def set_stub(self, port):
        self.channel= grpc.insecure_channel(f'{self.serverip}:{port}')
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)
        self.ringstub = rng.Ring.ring_pb2_grpc.RingElectionStub(self.channel)

    def __init__(self):
        self.reg_name = c.reg_name
        self.port = c.port
        c.init_client_data()


    def admin_cmd(self):
        global clear_screen
        self.commands = {
        "list-board": c.list_board,
        "set-node-time": lambda: self.set_node_time(),
        "set-timeout": lambda: self.set_timeout(),
        "restart": lambda: self.restart_game(),
        "": lambda: c.list_board,
        "countdown": lambda: print("countdown time:"),
        } 

        while True:
            cmd = input("Type your command: ")

            if cmd == "quit":
                print("Admin logout")
                sleep(1)
                break
            else:
                action = self.commands.get(cmd, lambda: print("No command found"))
                action()

    def restart_game(self):
        req = game_pb2.GameEmpty()
        try: 
            res = c.stub2.reset_data_call(req)
            print(res.message)
        except grpc.RpcError as e:
            print("server shutdown.")

    def set_node_time(self):
        port = input("which port would you like to set node time:")
        sec = input("which port would you like to set node time:")
        #self.set_stub(port=port)
        brkl.adjust_time_of_node(port,sec)
        print("time adjusted")

    def set_timeout(self):
        timeout = input("how many seconds for timeout?:")
        req = game_pb2.MessageRequest(message = timeout)
        response = c.stub2.set_timeout(req)
        print(f"set_timeout now: {response.message}")

c = Client()
a = None   

def run_ring_election():
    origin = 50051
    initial_message = rng.Ring.ring_pb2.RingMessage(
        origin=origin, max_id=origin, rounds=0, leader=-1)
    response = c.ringstub.StartElection(initial_message)
    return response.leader


if __name__ == "__main__": 
    c.access_to_server()
    list_tutorial()
    try:
        c.leader_message()
        c.list_board()
        if c.reg_symbol == "ADMIN":
            a = Admin()
            a.admin_cmd()
        else:
            list_game_cmd()
            c.start_game()
    except KeyboardInterrupt:
        print("you quit the game.")
        c.logout()
        sleep(1)
    
    c.logout()


