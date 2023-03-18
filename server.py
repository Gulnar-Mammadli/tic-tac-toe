import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc
import uuid

players = [None] * 2
first_port = 50051

class PlayerServiceServicer(game_pb2_grpc.PlayerServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.player1_symbol = 'X'
        self.player2_symbol = 'O'


    # draft
    def start_game(self, request, context):
        player_id = request.player_id
        if player_id in self.players:
            return game_pb2.GameId(game_id=self.players[player_id])
        else:
            game_id = str(uuid.uuid4())
            self.games[game_id] = {'board': [' '] * 9, 'next_player': 'X', 'winner': None}
            self.players[player_id] = game_id
            return game_pb2.GameId(game_id=game_id)

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

    def list_board(self, request, context):
        board_str = '\n'.join([' '.join(row) for row in self.board])
        return game_pb2.BoardResponse(board=board_str)
    
    def access_to_server(self, request, context):
        for i in range(len(players)):
            if not players[i]:
                players[i] = request.name
                id = request.name + str(i)
                symbol = self.player1_symbol  if i == 0 else self.player2_symbol 
                response = game_pb2.AccessResponse(id=id, symbol=symbol)
                return response
        # If both player slots are filled, return an error response
        context.set_details('All players are already in.')
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        return game_pb2.AccessResponse()


  
# class AdminServiceServicer(game_pb2_grpc.AdminServiceServicer):
#     def __init__(self) -> None:
#         super().__init__()

#     def waiting_for_players(self):
#         print(f"waiting at port {first_port}")

#     def start_game(self, request, context):
#         pass

#     def list_board(self, request, context):
#         pass

#admin = AdminServiceServicer()
player = PlayerServiceServicer()
def serve():
    #admin.waiting_for_players()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    game_pb2_grpc.add_PlayerServiceServicer_to_server(player, server)
    server.add_insecure_port(f'[::]:{first_port}')


    server.start()
    print(f'Starting server. Listening on port {first_port}.')

    server.wait_for_termination()




if __name__ == "__main__":
        serve()
        # player_id = request.player_id
        # game_id = self.players.get(player_id)
        # if game_id is None:
        #     context.set
