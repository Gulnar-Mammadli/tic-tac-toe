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
board = [[None, None, None], [None, None, None], [None, None, None]]
current_player = 0

game_board = {'1': ' ' , '2': ' ' , '3': ' ' ,
              '4': ' ' , '5': ' ' , '6': ' ' ,
              '7': ' ' , '8': ' ' , '9': ' '}

keys = []

for i in game_board:
    keys.append(i)

def printGameBoard(board = game_board):
    game_board = board['1'] + '|' + board['2'] + '|' + board['3'] + '\n'
    game_board += '-+-+-\n'
    game_board += board['4'] + '|' + board['5'] + '|' + board['6'] + '\n'
    game_board += '-+-+-\n'
    game_board += board['7'] + '|' + board['8'] + '|' + board['9'] + '\n'
    return game_board


class PlayerServiceServicer(game_pb2_grpc.PlayerServiceServicer):
    def __init__(self):
        self.player1_symbol = 'X'
        self.player2_symbol = 'O'

    async def list_board_async(self):
        async with grpc.aio.insecure_channel(f'{ip}:{first_port}') as channel:
            stub = game_pb2_grpc.AdminServiceStub(channel)
            response = await stub.list_board(game_pb2.GameEmpty())
            print(response.message)

    async def player_request(self, request, context):
        for i in range(len(players)):
            if not players[i]:
                id = request.name + str(i)
                symbol = self.player2_symbol if i == 0 else self.player1_symbol 
                response = game_pb2.AccessResponse(id=id, symbol=symbol)
                players[i] = response.id
                await self.list_board_async() # Replace this with your actual async method call
                return response

        # If both player slots are filled, return an error response
        context.set_details('All players are already in.')
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        return game_pb2.AccessResponse()
    
    def set_symbol(self, request, context):
        request = game_pb2.PlayerRequest()
        request_data = self.stub.set_symbol(request)
        if request_data.symbol not in [self.player1_symbol, self.player2_symbol]:
            context.set_details('Invalid symbol')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return game_pb2.SymbolResponse(success=False)
        if self.current_player != request_data.symbol:
            context.set_details('Not your turn')
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            return game_pb2.SymbolResponse(success=False)
        if self.board[request_data.row][request_data.col] != '-':
            context.set_details('Cell already occupied')
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            return game_pb2.SymbolResponse(success=False)

        self.board[request_data.row][request_data.col] = request_data.symbol
        if self.current_player == self.player1_symbol:
            self.current_player = self.player2_symbol
        else:
            self.current_player = self.player1_symbol
        return game_pb2.SymbolResponse(success=True)


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
        

    def join_game(self, request, context):
        player_id = request.player_id
        game_id = request.game_id
        if game_id not in self.games:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Game not found')
            return game_pb2.Empty()
        elif self.games[game_id]['winner'] is not None:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Game is over')
            return game_pb2.Empty()
        elif len([p for p in self.players.values() if p == game_id]) == 2:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Game is full')
            return game_pb2.Empty()
        else:
            self.players[player_id] = game_id
            return game_pb2.Empty()

    def make_move(self, request, context):
        player_id = request.player_id
        game_id = self.players.get(player_id)
        if game_id is None:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Player not in a game')
            return game_pb2.Empty()
        game = self.games.get(game_id)
        if game is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Game not found')
            return game_pb2.Empty()
        if game['winner'] is not None:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Game is over')
            return game_pb2.Empty()
        if player_id != game['next_player']:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Not player\'s turn')
            return game_pb2.Empty()
        pos = request.position
        if pos < 0 or pos > 8:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid position')
            return game_pb2.Empty()
        if game['board'][pos] != ' ':
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Position already taken')
            return game_pb2.Empty()
        game['board'][pos] = game['next_player']
        if self.check_for_win(game['board']):
            game['winner'] = game['next_player']
            return game_pb2.MoveResult(result=game_pb2.MoveResult.WIN)
        elif self.check_for_draw(game['board']):
            game['winner'] = 'DRAW'
            return game_pb2.MoveResult(result=game_pb2.MoveResult.DRAW)
        else:
            game['next_player'] = 'O' if game['next_player'] == 'X' else 'X'
            return game_pb2.MoveResult(result=game_pb2.MoveResult.CONTINUE)
    


    def access_to_server(self, request, context):
        for i in range(len(players)):
            if not players[i]:
                id = request.name + str(i)
                symbol = self.player2_symbol if i == 0 else self.player1_symbol 
                response = game_pb2.AccessResponse(id=id, symbol=symbol)
                players[i] = response.id
                return response
        # If both player slots are filled, return an error response
        context.set_details('All players are already in.')
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        return game_pb2.AccessResponse()
        
class AdminServiceServicer(game_pb2_grpc.AdminServiceServicer):
    def __init__(self) -> None:
        super().__init__()

    def waiting_for_players(self):
        print(f"waiting at port {first_port}")

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
        with grpc.insecure_channel(f'{ip}:{first_port}') as channel:
            stub = game_pb2_grpc.AdminServiceStub(channel)
            response = stub.list_board(game_pb2.GameEmpty())
            print(response.message)

    def list_board(self, request, context):
        return game_pb2.MessageResponse(message = printGameBoard())



admin = AdminServiceServicer()
player = PlayerServiceServicer()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    game_pb2_grpc.add_PlayerServiceServicer_to_server(player, server)
    game_pb2_grpc.add_AdminServiceServicer_to_server(admin, server)
    server.add_insecure_port(f'{ip_address}:{first_port}')

    # admin.waiting_for_players()

    server.start()
    print(f'Starting server. Listening on port {ip_address}:{first_port}.')
    # admin.list_board0()

    server.wait_for_termination()

if __name__ == "__main__":
        serve()
