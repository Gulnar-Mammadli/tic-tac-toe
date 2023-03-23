from time import sleep
import grpc
import game_pb2
import game_pb2_grpc
import datetime
from config import *
import time 
import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems (Linux, macOS)
        os.system('clear')

#import Berkeley.berkeley_utils as brkl
class Client():

    def __init__(self) -> None:
        self.reg_name = input("put your name here:")
        self.set_stub()
        self.reg_timestamp = str(datetime.datetime.now())
        self.total_processes = 3
        self.id = ""
        self.found_winner = False
        self.tie = False
    def set_stub(self):
        self.serverip = "localhost"  # input("paste ip here:")
        self.channel= grpc.insecure_channel(f'{self.serverip}:{first_port}')
        self.stub1 = game_pb2_grpc.PlayerServiceStub(self.channel)
        self.stub2 = game_pb2_grpc.AdminServiceStub(self.channel)

    def access_to_server(self):
        request = game_pb2.AccessRequest()
        request.name = self.reg_name
        response = self.stub1.access_to_server(request)
        self.id = response.id
        self.reg_symbol = response.symbol
        print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
        print(f"{response.game_status}")
        print(self.id[-1])
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
        print(f"Victory: {response.victory}")
        self.tie = response.symbol =="TIE!!"



    def check_status(self):
        request = game_pb2.GameEmpty()
        response = self.stub1.check_status(request)
        print(response.message)

    def check_winner(self):
        if self.found_winner == True:
            print(f"{self.found_winner} found winner")
        else:
            print(f"{self.found_winner} no winner")
            self.list_board()
        return self.found_winner

    def restart(self):
        self.found_winner = False
        request = game_pb2.AccessRequest(name = self.id)
        response = self.stub1.restart(request)
        print(f"your id: {response.id} symbol {response.symbol}")  # do something with the response object
        print(f"{response.game_status}")

    def start_election(self):
        print("start election")

    def start_election(self):
        print("start election")

    def sync_time(self):
        print("berkeley")

    def get_cmd(self):
        global clear_screen
        commands = {
        "ring": self.start_election,
        "berkeley": self.sync_time , 
        "board": self.list_board,
        "status": lambda: self.check_status,
        "": lambda: self.list_board,
        "countdown": lambda: print("countdown time:"),
        "cls" : lambda: clear_screen(),
        }


        while(True):

            if (self.check_winner() or self.tie):
                break
            start = time.time()    
            cmd = input("Type your command to the game master: ")
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

    
def list_tutorial():
    print("-----------------------------------------------")
    print("How to play the game: ")
    print("1. you will be assigned the symbol from the game master.")
    print("2. once it is your turn, just give the position at range 1-9.")
    print("3. or type other command.")
    print("------3.1. ""board"" to see current game board")
    print("------3.2. ""status"" or just press enter to check if it is your turn")
    print("------3.3. ""countdown"" time left over in your turn")
    print("------3.4. ""cls"" to clear the screen")
    print("------3.5. ""quit"" to left the game")
    print("-----------------------------------------------")




if __name__ == "__main__": 
    a = Client()
    a.access_to_server()
    a.list_board()
    list_tutorial()
    try:
        a.get_cmd()
    except KeyboardInterrupt:
        print("you quit the game.")
        a.logout()
        sleep(1)


