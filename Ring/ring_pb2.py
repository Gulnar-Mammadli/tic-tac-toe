# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ring.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nring.proto\x12\x0btic_tac_toe\" \n\rLeaderMessage\x12\x0f\n\x07message\x18\x01 \x01(\t\"M\n\x0bRingMessage\x12\x0e\n\x06origin\x18\x01 \x01(\x05\x12\x0e\n\x06max_id\x18\x02 \x01(\x05\x12\x0e\n\x06rounds\x18\x03 \x01(\x05\x12\x0e\n\x06leader\x18\x04 \x01(\x05\x32\xa1\x01\n\x0cRingElection\x12\x45\n\rStartElection\x12\x18.tic_tac_toe.RingMessage\x1a\x18.tic_tac_toe.RingMessage\"\x00\x12J\n\x0eleader_message\x12\x1a.tic_tac_toe.LeaderMessage\x1a\x1a.tic_tac_toe.LeaderMessage\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ring_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LEADERMESSAGE._serialized_start=27
  _LEADERMESSAGE._serialized_end=59
  _RINGMESSAGE._serialized_start=61
  _RINGMESSAGE._serialized_end=138
  _RINGELECTION._serialized_start=141
  _RINGELECTION._serialized_end=302
# @@protoc_insertion_point(module_scope)
