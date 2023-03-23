from config import *
import uuid
import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc
import time
#import ringserver as ring
#import Berkeley.berkeley_utils as brkl

players = [None] * 2
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
        board =""
    def set_symbol(self, request, context):
        pos = 0
        sym = request.symbol
        timpstp = ""
        if(self.current_turn != sym):
            pos = -1
            board = f"it's not your turn. please wait {sym}"
        else:
            global game_board
            if game_board[request.position] == ' ':
                
                pos = request.position
                game_board[pos] = sym
                self.current_turn = self.player2_symbol if self.current_turn == self.player1_symbol else self.player1_symbol
                board = printGameBoard()
                if self.check_victory(sym,pos): 
                    sym = f"{request.symbol} WON!!"
                print(admin.list_board0())
            else:   
                pos = -1
                board = f"{request.position} is invalid position. use other number instead"
        response = game_pb2.PlayerResponse(position=pos, symbol=sym,timestamp = "", game_board =board, victory = self.check_victory(sym,pos))
        return response
    
    def check_victory(self, player_symbol, pos):
        global winning_combinations
        for combination in winning_combinations:
            if all(game_board[pos] == player_symbol for pos in combination):
                return True
        return False


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
            index = players.index(request.message)
            players[index] = None
        player_count -= 1
        response = game_pb2.MessageResponse(message = left)
        return response
    
    def access_to_server(self, request, context):
        for i in range(len(players)):
            if not players[i]:
                global player_count
                player_count += 1 
                sttatus = "wait for another player" if player_count == 1 else "both you and another player are in. please type ready to start the game"
                id = request.name + str(i)
                symbol = self.player2_symbol if i == 0 else self.player1_symbol 
                response = game_pb2.AccessResponse(id=id, symbol=symbol,game_status = sttatus)
                players[i] = response.id
                print(f"{players[i]} has joined the game.")


                return response
        # If both player slots are filled, return an error response
        context.set_details('All players are already in.')
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        return game_pb2.AccessResponse()
        
class AdminServiceServicer(game_pb2_grpc.AdminServiceServicer):
    def __init__(self) -> None:
        super().__init__()

    def waiting_for_players(self):
        return (f"waiting for another player at port {first_port}")
 
    # def start_game(self, request, context):
    #         response = game_pb2.MessageResponse(board=game_board)
    #         return response

    def check_winner(self):
        pass

    def broadcastMessage(self,request,context):
            for i in range(len(players)):
                yield game_pb2.MessageResponse(message=f"{request.message} {i}")
                time.sleep(1)
    
    def list_board0(self):
        with grpc.insecure_channel(f'[::]:{first_port}') as channel:
            stub = game_pb2_grpc.AdminServiceStub(channel)
            response = stub.list_board(game_pb2.GameEmpty())
            return response.message

    def list_board(self, request, context):
        return game_pb2.MessageResponse(message = printGameBoard())
    
admin = AdminServiceServicer()
player = PlayerServiceServicer()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    game_pb2_grpc.add_PlayerServiceServicer_to_server(player, server)
    game_pb2_grpc.add_AdminServiceServicer_to_server(admin, server)
    server.add_insecure_port(f'[::]:{first_port}')

    # admin.waiting_for_players()

    server.start()
    print(f'Starting server. Listening on port {ip_address}:{first_port}.')
    print(admin.list_board0())

    server.wait_for_termination()

if __name__ == "__main__":
        serve()
