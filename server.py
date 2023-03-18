import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc

players = [None] * 2
first_port = 50051

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
    
    def access_to_server(self, request, context):
        for i in range(len(players)):
            if not players[i]:
                players[i] = request.name
                id = request.name + str(i)
                symbol = "o" if i == 0 else "x"
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