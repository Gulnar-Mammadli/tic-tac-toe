from config import *
import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc
import time
import Ring.ring_utils as rng
import Berkeley.berkeley_utils as brkl

players = [None] * 2
players_ingame = [False] * 2
player_count = 0

game_board = {1: ' ' , 2: ' ' , 3: ' ' ,
              4: ' ' , 5: ' ' , 6: ' ' ,
              7: ' ' , 8: ' ' , 9: ' '}

winning_combinations = [
    [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Rows
    [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Columns
    [1, 5, 9], [3, 5, 7]             # Diagonals
]

keys = []

for i in game_board:
    keys.append(i)

def printGameBoard(board = game_board):
    game_board = board[1] + '|' + board[2] + '|' + board[3] + '\n'
    game_board += '-+-+-\n'
    game_board += board[4] + '|' + board[5] + '|' + board[6] + '\n'
    game_board += '-+-+-\n'
    game_board += board[7] + '|' + board[8] + '|' + board[9] + '\n'
    return game_board



class PlayerServiceServicer(game_pb2_grpc.PlayerServiceServicer):
    def __init__(self):
        self.player1_symbol = 'X'
        self.player2_symbol = 'O'
        self.current_turn = self.player2_symbol
        self.board =""
        self.found_winner = False
        self.counter = 0
        self.winner = ""
        self.leader = 0

    def set_symbol(self, request, context):
        pos = 0
        sym = request.symbol
        timpstp = request.timestamp

        global players_ingame
        if players_ingame[0] == False or players_ingame[1] == False:
            pos = -1
            board = f"wait for another player"
        if int(timpstp) > time_limit:
            pos = -2
            board = f"timeout" 
            self.current_turn = self.player2_symbol if self.current_turn == self.player1_symbol else self.player1_symbol

        if(self.current_turn != sym):
            pos = -1
            board = f"it's not your turn. please wait {sym}"

        else:
            if self.counter >= 9:
                self.found_winner = False 
                sym = f"TIE!!"
                board = printGameBoard()
            global game_board
            if game_board[request.position] == ' ':
                self.counter += 1
                pos = request.position
                game_board[pos] = sym
                self.current_turn = self.player2_symbol if self.current_turn == self.player1_symbol else self.player1_symbol
                board = printGameBoard()
                if self.check_victory(sym,pos):
                    self.found_winner = True 
                    self.winner = request.symbol
                    sym = f"{request.symbol} WON!!"
                    players_ingame= [False for _ in players_ingame]
                print(board)
            else:   
                pos = -1
                board = f"{request.position} is invalid position. use other number instead"
        response = game_pb2.PlayerResponse(position=pos, symbol=sym,timestamp = "", game_board =board, victory = self.found_winner)
        

        return response
    
    def check_victory(self, player_symbol, pos):
        global winning_combinations
        for combination in winning_combinations:
            if all(game_board[pos] == player_symbol for pos in combination):
                return True
        return False

    def reset_data(self):
        for key in keys:
            game_board[key] = " "
        self.current_turn = self.player2_symbol
        self.board =""
        self.found_winner = False
        self.counter = 0
        self.winner = ""
        global players_ingame
        players_ingame[0] = False
        players_ingame[1] = False

    def restart(self, request, context):
        self.reset_data()
        global players_ingame
        players_ingame[int(request.name[-1])] = True
        response = game_pb2.AccessResponse()
        response.id = request.name
        response.symbol = self.player2_symbol if request.name[-1] == "0" else self.player1_symbol
        response.game_status = "wait for another player" if players_ingame[0] == True and players_ingame[1] == True else "both you and another player are in"
        print(f"{request.name} REQUESTS RESTART GAME")
        return response
    
    def start_game(self):
        #based on the document, this method includes:
        # 1. Berkeley Clock
        # 2. Ring Election
        # 3. Start tic-tac-toe  
        player_id = self.player_id
        if player_id in self.players:
            print(f": This is the game board. Player {player_id} , you can start playing the game")
            self.board = {'board': [' '] * 9, 'first_player': 'X', 'winner': None}
            #return game_pb2.
    
    def logout(self, request, context):
        left = f"{request.message} has left the game"
        print(left)
        if request.message  in players:
            global players_ingame
            index = players.index(request.message)
            players[index] = None
            players_ingame[index] = False
        global player_count
        player_count -= 1
        response = game_pb2.MessageResponse(message = left)
        return response
    
    def access_to_server(self, request, context):
        for i in range(len(players)):
            if not players[i]:
                global player_count
                player_count += 1 
                sttatus = "wait for another player" if player_count == 1 else "both you and another player are in."
                id = request.name + str(i)
                symbol = self.player2_symbol if i == 0 else self.player1_symbol 
                response = game_pb2.AccessResponse(id=id, symbol=symbol,game_status = sttatus)
                players[i] = response.id
                players_ingame[i] = True
                print(f"{players[i]} has joined the game.")


                return response
        # If both player slots are filled, return an error response
        context.set_details('All players are already in.')
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        return game_pb2.AccessResponse()
    
    def leader_message(self, request, context):
        self.leader = int(request.message)
        ring.leader_port = int(request.message)
        response = game_pb2.MessageResponse(message = str(ring.leader_port))
        return response
    
class AdminServiceServicer(game_pb2_grpc.AdminServiceServicer):
    def __init__(self) -> None:
        super().__init__()

    def waiting_for_players(self):
        return (f"waiting for another player at port {first_port}")
 
    def broadcastMessage(self,request,context):
            for i in range(len(players)):
                yield game_pb2.MessageResponse(message=f"{request.message} {i}")
                time.sleep(1)
    
    def list_board0(self):
        print(printGameBoard())

    def list_board(self, request, context):
        return game_pb2.MessageResponse(message = printGameBoard())
    


admin = AdminServiceServicer()
player = PlayerServiceServicer()
server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
port1, port2,address,next_node_address = "","",0,0
ring = None

def serve_ring():
    global ring
    ring = rng.RingElectionServicer(address)
    rng.Ring.ring_pb2_grpc.add_RingElectionServicer_to_server(ring, server)
    ring.set_next_node(next_node_address)

def serve():
    game_pb2_grpc.add_PlayerServiceServicer_to_server(player, server)
    game_pb2_grpc.add_AdminServiceServicer_to_server(admin, server)

    server.start()
    print(f'Starting server. Listening on port {ip_address}:{address}.')

    server.wait_for_termination()

if __name__ == "__main__":
    port1 = input("Please put your port id:")
    port2 = int(port1) + 1 if int(port1) < first_port + total_processes - 1 else first_port
    address = int(port1)
    next_node_address = int(port2)
    server.add_insecure_port(f'[::]:{address}')
    serve_ring()
    serve()

