# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import data_pb2 as data__pb2

class TaskDataTransmitServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.TransmitTaskData = channel.unary_unary(
                '/TaskServer.TaskDataTransmitService/TransmitTaskData',
                request_serializer=data__pb2.TransmitTaskDataRequest.SerializeToString,
                response_deserializer=data__pb2.TransmitTaskDataResponse.FromString,
                )


class TaskDataTransmitServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def TransmitTaskData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TaskDataTransmitServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'TransmitTaskData': grpc.unary_unary_rpc_method_handler(
                    servicer.TransmitTaskData,
                    request_deserializer=data__pb2.TransmitTaskDataRequest.FromString,
                    response_serializer=data__pb2.TransmitTaskDataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TaskServer.TaskDataTransmitService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TaskDataTransmitService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def TransmitTaskData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TaskServer.TaskDataTransmitService/TransmitTaskData',
            data__pb2.TransmitTaskDataRequest.SerializeToString,
            data__pb2.TransmitTaskDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)