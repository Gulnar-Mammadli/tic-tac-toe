import grpc
from concurrent import futures
import game_pb2
import game_pb2_grpc



class PlayerServiceServicer(game_pb2_grpc.PlayerServiceServicer):
    def __init__(self) -> None:
        super().__init__()

    def set_symbol(self, request, context):
        pass
    
    def list_board(self, request, context):
        pass

# Increase the maximum metadata size
options = [
    ('grpc.max_send_message_length', 50 * 1024 * 1024),  # 50 MB
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB
]

def serve():
    player_service_servicer = PlayerServiceServicer()