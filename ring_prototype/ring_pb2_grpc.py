# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import ring_pb2 as ring__pb2


class RingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PassMessage = channel.unary_unary(
                '/ring.Ring/PassMessage',
                request_serializer=ring__pb2.Message.SerializeToString,
                response_deserializer=ring__pb2.Message.FromString,
                )


class RingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PassMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PassMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.PassMessage,
                    request_deserializer=ring__pb2.Message.FromString,
                    response_serializer=ring__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ring.Ring', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Ring(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PassMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ring.Ring/PassMessage',
            ring__pb2.Message.SerializeToString,
            ring__pb2.Message.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
