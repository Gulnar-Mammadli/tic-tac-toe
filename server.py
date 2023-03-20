import uuid
import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc
import time

players = [None] * 2
board = [[None, None, None], [None, None, None], [None, None, None]]
current_player = 0
first_port = 50051

class PlayerServiceServicer(game_pb2_grpc.PlayerServiceServicer):
    def __init__(self) -> None:
        super().__init__()
        self.board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
        # self.player1_symbol = 'X'
        # self.player2_symbol = 'O'

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

    def list_board(self, request, context):
        board_str = '\n'.join([' '.join(row) for row in self.board])
        return game_pb2.BoardResponse(board=board_str)
    
    def access_to_server(self, request, context):
        for i in range(len(players)):
            if not players[i]:
                id = request.name + str(i)
                symbol = "o" if i == 0 else "x"
                response = game_pb2.AccessResponse(id=id, symbol=symbol)
                players[i] = response.id
                return response
        # If both player slots are filled, return an error response
        context.set_details('All players are already in.')
        context.set_code(grpc.StatusCode.UNAVAILABLE)
        return game_pb2.AccessResponse()


  

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


class AdminServiceServicer(game_pb2_grpc.AdminServiceServicer):
    def __init__(self) -> None:
        super().__init__()

    def waiting_for_players(self):
        print(f"waiting at port {first_port}")

    def list_board(self, request, context):
        pass


    def start_game(self, request, context):
            # Check if both players have joined
            if None in players:
                context.set_details('Waiting for players to join.')
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                return game_pb2.GameResponse()

            # Check if the current player is allowed to make a move
            if players[current_player] != request.id[:-1]:
                context.set_details('It is not your turn.')
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                return game_pb2.GameResponse()

            # Check if the requested move is valid
            row, col = int(request.move[0]), int(request.move[1])
            if board[row][col] is not None:
                context.set_details('Invalid move.')
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return game_pb2.GameResponse()

            # Update the game board
            board[row][col] = players[current_player]

            # Check if the current player has won
            # winner = check_winner()
            # if winner:
            #     response = game_pb2.GameResponse(result=winner + ' wins!')
            #     # self.reset_game()
            #     return response

            # # Check if the game has ended in a tie
            # if self.check_tie():
            #     response = game_pb2.GameResponse(result='Tie game.')
            #     self.reset_game()
            #     return response

            # Update the current player and return the game board
            current_player = 1 - current_player
            board_str = '\n'.join([' '.join(row) for row in board])
            response = game_pb2.GameResponse(board=board_str)
            return response

    def check_winner(self):
            # Check rows
            for row in board:
                if row[0] == row[1] == row[2] and row[0] is not None:
                    return row[0]

            # Check columns
            for col in range(3):
                if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
                    return board[0][col]

            # Check diagonals
            if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
                return board[0][0]
            if board[0][2] == self.board[1][1] == board[2][0] and board[0][2] is not None:
                return board[0][2]

            return None

    def broadcastMessage(self,request,context):
            for i in range(len(players)):
                yield game_pb2.MessageResponse(message=f"{request.message} {i}")
                time.sleep(1)






if __name__ == "__main__":
        serve()
        
        # player_id = request.player_id
        # game_id = self.players.get(player_id)
        # if game_id is None:
        #     context.set
