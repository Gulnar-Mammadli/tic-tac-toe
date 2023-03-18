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

    def list_board(self, request, context):
        board_str = '\n'.join([' '.join(row) for row in self.board])
        return game_pb2.BoardResponse(board=board_str)
