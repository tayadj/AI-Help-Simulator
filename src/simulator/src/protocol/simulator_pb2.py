# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: simulator.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'simulator.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fsimulator.proto\x12\tsimulator\"\x1b\n\x0b\x41udioStream\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"{\n\x0fHistoryResponse\x12\x38\n\x07history\x18\x01 \x03(\x0b\x32\'.simulator.HistoryResponse.HistoryEntry\x1a.\n\x0cHistoryEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x10\n\x0eHistoryRequest\"\x1f\n\rPromptRequest\x12\x0e\n\x06prompt\x18\x01 \x01(\t\" \n\x0ePromptResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2\xec\x01\n\x10SimulatorService\x12\x41\n\x0bStreamAudio\x12\x16.simulator.AudioStream\x1a\x16.simulator.AudioStream(\x01\x30\x01\x12O\n\x16GetConversationHistory\x12\x19.simulator.HistoryRequest\x1a\x1a.simulator.HistoryResponse\x12\x44\n\rReceivePrompt\x12\x18.simulator.PromptRequest\x1a\x19.simulator.PromptResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'simulator_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HISTORYRESPONSE_HISTORYENTRY']._loaded_options = None
  _globals['_HISTORYRESPONSE_HISTORYENTRY']._serialized_options = b'8\001'
  _globals['_AUDIOSTREAM']._serialized_start=30
  _globals['_AUDIOSTREAM']._serialized_end=57
  _globals['_HISTORYRESPONSE']._serialized_start=59
  _globals['_HISTORYRESPONSE']._serialized_end=182
  _globals['_HISTORYRESPONSE_HISTORYENTRY']._serialized_start=136
  _globals['_HISTORYRESPONSE_HISTORYENTRY']._serialized_end=182
  _globals['_HISTORYREQUEST']._serialized_start=184
  _globals['_HISTORYREQUEST']._serialized_end=200
  _globals['_PROMPTREQUEST']._serialized_start=202
  _globals['_PROMPTREQUEST']._serialized_end=233
  _globals['_PROMPTRESPONSE']._serialized_start=235
  _globals['_PROMPTRESPONSE']._serialized_end=267
  _globals['_SIMULATORSERVICE']._serialized_start=270
  _globals['_SIMULATORSERVICE']._serialized_end=506
# @@protoc_insertion_point(module_scope)
