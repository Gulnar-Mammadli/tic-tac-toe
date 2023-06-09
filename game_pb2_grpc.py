# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import game_pb2 as game__pb2


class PlayerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.restart = channel.unary_unary(
                '/tic_tac_toe.PlayerService/restart',
                request_serializer=game__pb2.AccessRequest.SerializeToString,
                response_deserializer=game__pb2.AccessResponse.FromString,
                )
        self.check_status = channel.unary_unary(
                '/tic_tac_toe.PlayerService/check_status',
                request_serializer=game__pb2.GameEmpty.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )
        self.set_symbol = channel.unary_unary(
                '/tic_tac_toe.PlayerService/set_symbol',
                request_serializer=game__pb2.PlayerRequest.SerializeToString,
                response_deserializer=game__pb2.PlayerResponse.FromString,
                )
        self.access_to_server = channel.unary_unary(
                '/tic_tac_toe.PlayerService/access_to_server',
                request_serializer=game__pb2.AccessRequest.SerializeToString,
                response_deserializer=game__pb2.AccessResponse.FromString,
                )
        self.logout = channel.unary_unary(
                '/tic_tac_toe.PlayerService/logout',
                request_serializer=game__pb2.MessageRequest.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )
        self.leader_message = channel.unary_unary(
                '/tic_tac_toe.PlayerService/leader_message',
                request_serializer=game__pb2.MessageRequest.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )


class PlayerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def restart(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def check_status(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set_symbol(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def access_to_server(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def logout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def leader_message(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PlayerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'restart': grpc.unary_unary_rpc_method_handler(
                    servicer.restart,
                    request_deserializer=game__pb2.AccessRequest.FromString,
                    response_serializer=game__pb2.AccessResponse.SerializeToString,
            ),
            'check_status': grpc.unary_unary_rpc_method_handler(
                    servicer.check_status,
                    request_deserializer=game__pb2.GameEmpty.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
            'set_symbol': grpc.unary_unary_rpc_method_handler(
                    servicer.set_symbol,
                    request_deserializer=game__pb2.PlayerRequest.FromString,
                    response_serializer=game__pb2.PlayerResponse.SerializeToString,
            ),
            'access_to_server': grpc.unary_unary_rpc_method_handler(
                    servicer.access_to_server,
                    request_deserializer=game__pb2.AccessRequest.FromString,
                    response_serializer=game__pb2.AccessResponse.SerializeToString,
            ),
            'logout': grpc.unary_unary_rpc_method_handler(
                    servicer.logout,
                    request_deserializer=game__pb2.MessageRequest.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
            'leader_message': grpc.unary_unary_rpc_method_handler(
                    servicer.leader_message,
                    request_deserializer=game__pb2.MessageRequest.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tic_tac_toe.PlayerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PlayerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def restart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.PlayerService/restart',
            game__pb2.AccessRequest.SerializeToString,
            game__pb2.AccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def check_status(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.PlayerService/check_status',
            game__pb2.GameEmpty.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set_symbol(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.PlayerService/set_symbol',
            game__pb2.PlayerRequest.SerializeToString,
            game__pb2.PlayerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def access_to_server(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.PlayerService/access_to_server',
            game__pb2.AccessRequest.SerializeToString,
            game__pb2.AccessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def logout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.PlayerService/logout',
            game__pb2.MessageRequest.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def leader_message(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.PlayerService/leader_message',
            game__pb2.MessageRequest.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class AdminServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.admin_request = channel.unary_unary(
                '/tic_tac_toe.AdminService/admin_request',
                request_serializer=game__pb2.GameEmpty.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )
        self.reset_data_call = channel.unary_unary(
                '/tic_tac_toe.AdminService/reset_data_call',
                request_serializer=game__pb2.GameEmpty.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )
        self.start_game = channel.unary_unary(
                '/tic_tac_toe.AdminService/start_game',
                request_serializer=game__pb2.PlayerRequest.SerializeToString,
                response_deserializer=game__pb2.PlayerResponse.FromString,
                )
        self.set_timeout = channel.unary_unary(
                '/tic_tac_toe.AdminService/set_timeout',
                request_serializer=game__pb2.MessageRequest.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )
        self.list_board = channel.unary_unary(
                '/tic_tac_toe.AdminService/list_board',
                request_serializer=game__pb2.GameEmpty.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )
        self.broadcastMessage = channel.unary_stream(
                '/tic_tac_toe.AdminService/broadcastMessage',
                request_serializer=game__pb2.MessageRequest.SerializeToString,
                response_deserializer=game__pb2.MessageResponse.FromString,
                )


class AdminServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def admin_request(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def reset_data_call(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def start_game(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def set_timeout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list_board(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def broadcastMessage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AdminServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'admin_request': grpc.unary_unary_rpc_method_handler(
                    servicer.admin_request,
                    request_deserializer=game__pb2.GameEmpty.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
            'reset_data_call': grpc.unary_unary_rpc_method_handler(
                    servicer.reset_data_call,
                    request_deserializer=game__pb2.GameEmpty.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
            'start_game': grpc.unary_unary_rpc_method_handler(
                    servicer.start_game,
                    request_deserializer=game__pb2.PlayerRequest.FromString,
                    response_serializer=game__pb2.PlayerResponse.SerializeToString,
            ),
            'set_timeout': grpc.unary_unary_rpc_method_handler(
                    servicer.set_timeout,
                    request_deserializer=game__pb2.MessageRequest.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
            'list_board': grpc.unary_unary_rpc_method_handler(
                    servicer.list_board,
                    request_deserializer=game__pb2.GameEmpty.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
            'broadcastMessage': grpc.unary_stream_rpc_method_handler(
                    servicer.broadcastMessage,
                    request_deserializer=game__pb2.MessageRequest.FromString,
                    response_serializer=game__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tic_tac_toe.AdminService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AdminService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def admin_request(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.AdminService/admin_request',
            game__pb2.GameEmpty.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def reset_data_call(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.AdminService/reset_data_call',
            game__pb2.GameEmpty.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def start_game(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.AdminService/start_game',
            game__pb2.PlayerRequest.SerializeToString,
            game__pb2.PlayerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def set_timeout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.AdminService/set_timeout',
            game__pb2.MessageRequest.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list_board(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tic_tac_toe.AdminService/list_board',
            game__pb2.GameEmpty.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def broadcastMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/tic_tac_toe.AdminService/broadcastMessage',
            game__pb2.MessageRequest.SerializeToString,
            game__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
