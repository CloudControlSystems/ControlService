# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndata.proto\x12\nTaskServer\"B\n\x17TransmitTaskDataRequest\x12\x11\n\ttaskOrder\x18\x01 \x01(\r\x12\x14\n\x0ctransmitData\x18\x02 \x01(\x0c\">\n\x18TransmitTaskDataResponse\x12\x0e\n\x06result\x18\x01 \x01(\r\x12\x12\n\nvolumePath\x18\x02 \x01(\t2x\n\x17TaskDataTransmitService\x12]\n\x10TransmitTaskData\x12#.TaskServer.TransmitTaskDataRequest\x1a$.TaskServer.TransmitTaskDataResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRANSMITTASKDATAREQUEST._serialized_start=26
  _TRANSMITTASKDATAREQUEST._serialized_end=92
  _TRANSMITTASKDATARESPONSE._serialized_start=94
  _TRANSMITTASKDATARESPONSE._serialized_end=156
  _TASKDATATRANSMITSERVICE._serialized_start=158
  _TASKDATATRANSMITSERVICE._serialized_end=278
# @@protoc_insertion_point(module_scope)
