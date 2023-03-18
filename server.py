import uuid
import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc



class PlayerServiceServicer(game_pb2_grpc.PlayerServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        self.player1_symbol = 'X'
        self.player2_symbol = 'O'
        self.current_player = self.player1_symbol
        self.games = {}
        self.players = {}

    def set_symbol(self, request, context):
        if request.symbol not in [self.player1_symbol, self.player2_symbol]:
            context.set_details('Invalid symbol')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return game_pb2.SymbolResponse(success=False)
        if self.current_player != request.symbol:
            context.set_details('Not your turn')
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            return game_pb2.SymbolResponse(success=False)
        if self.board[request.row][request.col] != '-':
            context.set_details('Cell already occupied')
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            return game_pb2.SymbolResponse(success=False)

        self.board[request.row][request.col] = request.symbol
        if self.current_player == self.player1_symbol:
            self.current_player = self.player2_symbol
        else:
            self.current_player = self.player1_symbol
        return game_pb2.SymbolResponse(success=True)


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
        player_id = request.player_id
        game_id = self.players.get(player_id)
        if game_id is None:
            context.set
