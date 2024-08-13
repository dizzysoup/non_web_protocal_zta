# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: credentials.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x63redentials.proto\x12\x0b\x63redentials\"\x1b\n\nJWTRequest\x12\r\n\x05token\x18\x01 \x01(\t\"\x85\x02\n\x11PublicKeyResponse\x12\x13\n\x0b\x61ttestation\x18\x01 \x01(\t\x12\x43\n\x16\x61uthenticatorSelection\x18\x02 \x01(\x0b\x32#.credentials.AuthenticatorSelection\x12\x11\n\tchallenge\x18\x03 \x01(\t\x12\x36\n\x10pubKeyCredParams\x18\x04 \x03(\x0b\x32\x1c.credentials.PubKeyCredParam\x12\x1b\n\x02rp\x18\x05 \x01(\x0b\x32\x0f.credentials.RP\x12\x1f\n\x04user\x18\x06 \x01(\x0b\x32\x11.credentials.User\x12\r\n\x05token\x18\x07 \x01(\t\",\n\x0fPubKeyCredParam\x12\x0b\n\x03\x61lg\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\t\"\x84\x01\n\x16\x41uthenticatorSelection\x12\x1f\n\x17\x61uthenticatorAttachment\x18\x01 \x01(\t\x12\x1a\n\x12requireResidentKey\x18\x02 \x01(\x08\x12\x13\n\x0bresidentKey\x18\x03 \x01(\t\x12\x18\n\x10userVerification\x18\x04 \x01(\t\"\x1e\n\x02RP\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\" \n\x04User\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x16\n\x07Message\x12\x0b\n\x03msg\x18\x01 \x01(\t\"\x1a\n\nMsgRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"H\n\tPublicKey\x12\x0b\n\x03kty\x18\x01 \x01(\x05\x12\x0b\n\x03\x61lg\x18\x02 \x01(\x05\x12\x0b\n\x03\x63rv\x18\x03 \x01(\x05\x12\t\n\x01x\x18\x04 \x01(\t\x12\t\n\x01y\x18\x05 \x01(\t\"\x9f\x01\n\x11\x43redentialRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12*\n\npublic_key\x18\x02 \x01(\x0b\x32\x16.credentials.PublicKey\x12\x12\n\nsign_count\x18\x03 \x01(\x05\x12\x12\n\ntransports\x18\x04 \x01(\t\x12\x0e\n\x06\x61\x61guid\x18\x05 \x01(\t\x12\x15\n\rcredential_id\x18\x06 \x01(\t\"\x1c\n\tLogoutMsg\x12\x0f\n\x07message\x18\x01 \x01(\t\"6\n\x0cRPCheckReply\x12\x15\n\ris_registered\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"%\n\x12\x43redentialResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\" \n\x0cHelloRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"\x1e\n\rHelloResponse\x12\r\n\x05reply\x18\x01 \x01(\t2\x83\x02\n\x11\x43redentialService\x12R\n\x0fStoreCredential\x12\x1e.credentials.CredentialRequest\x1a\x1f.credentials.CredentialResponse\x12W\n\x14SendCredentialToAuth\x12\x1e.credentials.CredentialRequest\x1a\x1f.credentials.CredentialResponse\x12\x41\n\x06Logout\x12\x16.credentials.LogoutMsg\x1a\x1f.credentials.CredentialResponse2]\n\x10RPManagerService\x12I\n\x13\x43heckRPRegistration\x12\x17.credentials.MsgRequest\x1a\x19.credentials.RPCheckReply2\xeb\x01\n\x15\x41uthenticationService\x12H\n\rRegisterBegin\x12\x17.credentials.MsgRequest\x1a\x1e.credentials.PublicKeyResponse\x12\x41\n\x10RegisterComplete\x12\x17.credentials.JWTRequest\x1a\x14.credentials.Message\x12\x45\n\nLoginBegin\x12\x17.credentials.MsgRequest\x1a\x1e.credentials.PublicKeyResponse2V\n\x0fgrpctestService\x12\x43\n\nHelloWorld\x12\x19.credentials.HelloRequest\x1a\x1a.credentials.HelloResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'credentials_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_JWTREQUEST']._serialized_start=34
  _globals['_JWTREQUEST']._serialized_end=61
  _globals['_PUBLICKEYRESPONSE']._serialized_start=64
  _globals['_PUBLICKEYRESPONSE']._serialized_end=325
  _globals['_PUBKEYCREDPARAM']._serialized_start=327
  _globals['_PUBKEYCREDPARAM']._serialized_end=371
  _globals['_AUTHENTICATORSELECTION']._serialized_start=374
  _globals['_AUTHENTICATORSELECTION']._serialized_end=506
  _globals['_RP']._serialized_start=508
  _globals['_RP']._serialized_end=538
  _globals['_USER']._serialized_start=540
  _globals['_USER']._serialized_end=572
  _globals['_MESSAGE']._serialized_start=574
  _globals['_MESSAGE']._serialized_end=596
  _globals['_MSGREQUEST']._serialized_start=598
  _globals['_MSGREQUEST']._serialized_end=624
  _globals['_PUBLICKEY']._serialized_start=626
  _globals['_PUBLICKEY']._serialized_end=698
  _globals['_CREDENTIALREQUEST']._serialized_start=701
  _globals['_CREDENTIALREQUEST']._serialized_end=860
  _globals['_LOGOUTMSG']._serialized_start=862
  _globals['_LOGOUTMSG']._serialized_end=890
  _globals['_RPCHECKREPLY']._serialized_start=892
  _globals['_RPCHECKREPLY']._serialized_end=946
  _globals['_CREDENTIALRESPONSE']._serialized_start=948
  _globals['_CREDENTIALRESPONSE']._serialized_end=985
  _globals['_HELLOREQUEST']._serialized_start=987
  _globals['_HELLOREQUEST']._serialized_end=1019
  _globals['_HELLORESPONSE']._serialized_start=1021
  _globals['_HELLORESPONSE']._serialized_end=1051
  _globals['_CREDENTIALSERVICE']._serialized_start=1054
  _globals['_CREDENTIALSERVICE']._serialized_end=1313
  _globals['_RPMANAGERSERVICE']._serialized_start=1315
  _globals['_RPMANAGERSERVICE']._serialized_end=1408
  _globals['_AUTHENTICATIONSERVICE']._serialized_start=1411
  _globals['_AUTHENTICATIONSERVICE']._serialized_end=1646
  _globals['_GRPCTESTSERVICE']._serialized_start=1648
  _globals['_GRPCTESTSERVICE']._serialized_end=1734
# @@protoc_insertion_point(module_scope)
