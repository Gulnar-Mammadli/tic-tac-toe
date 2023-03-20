import ring_pb2
import ring_pb2_grpc

class RingElectionServicer(ring_pb2_grpc.RingElectionServicer):
    def __init__(self) -> None:
        super().__init__()
        