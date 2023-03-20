import Ring.ring_pb2 as ring_pb2
import Ring.ring_pb2_grpc as ring_pb2_grpc

class RingElectionServicer(ring_pb2_grpc.RingElectionServicer):
    def __init__(self) -> None:
        super().__init__()
        
