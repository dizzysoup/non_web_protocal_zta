# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import credentials_pb2 as credentials__pb2

GRPC_GENERATED_VERSION = '1.64.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in credentials_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class CredentialServiceStub(object):
    """憑證服務
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StoreCredential = channel.unary_unary(
                '/credentials.CredentialService/StoreCredential',
                request_serializer=credentials__pb2.CredentialRequest.SerializeToString,
                response_deserializer=credentials__pb2.CredentialResponse.FromString,
                _registered_method=True)
        self.SendCredentialToAuth = channel.unary_unary(
                '/credentials.CredentialService/SendCredentialToAuth',
                request_serializer=credentials__pb2.CredentialRequest.SerializeToString,
                response_deserializer=credentials__pb2.CredentialResponse.FromString,
                _registered_method=True)
        self.Logout = channel.unary_unary(
                '/credentials.CredentialService/Logout',
                request_serializer=credentials__pb2.LogoutMsg.SerializeToString,
                response_deserializer=credentials__pb2.CredentialResponse.FromString,
                _registered_method=True)


class CredentialServiceServicer(object):
    """憑證服務
    """

    def StoreCredential(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendCredentialToAuth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Logout(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CredentialServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StoreCredential': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreCredential,
                    request_deserializer=credentials__pb2.CredentialRequest.FromString,
                    response_serializer=credentials__pb2.CredentialResponse.SerializeToString,
            ),
            'SendCredentialToAuth': grpc.unary_unary_rpc_method_handler(
                    servicer.SendCredentialToAuth,
                    request_deserializer=credentials__pb2.CredentialRequest.FromString,
                    response_serializer=credentials__pb2.CredentialResponse.SerializeToString,
            ),
            'Logout': grpc.unary_unary_rpc_method_handler(
                    servicer.Logout,
                    request_deserializer=credentials__pb2.LogoutMsg.FromString,
                    response_serializer=credentials__pb2.CredentialResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'credentials.CredentialService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('credentials.CredentialService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CredentialService(object):
    """憑證服務
    """

    @staticmethod
    def StoreCredential(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.CredentialService/StoreCredential',
            credentials__pb2.CredentialRequest.SerializeToString,
            credentials__pb2.CredentialResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SendCredentialToAuth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.CredentialService/SendCredentialToAuth',
            credentials__pb2.CredentialRequest.SerializeToString,
            credentials__pb2.CredentialResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Logout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.CredentialService/Logout',
            credentials__pb2.LogoutMsg.SerializeToString,
            credentials__pb2.CredentialResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class RPManagerServiceStub(object):
    """存取RP 相關服務
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckRPRegistration = channel.unary_unary(
                '/credentials.RPManagerService/CheckRPRegistration',
                request_serializer=credentials__pb2.MsgRequest.SerializeToString,
                response_deserializer=credentials__pb2.RPCheckReply.FromString,
                _registered_method=True)


class RPManagerServiceServicer(object):
    """存取RP 相關服務
    """

    def CheckRPRegistration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RPManagerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CheckRPRegistration': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckRPRegistration,
                    request_deserializer=credentials__pb2.MsgRequest.FromString,
                    response_serializer=credentials__pb2.RPCheckReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'credentials.RPManagerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('credentials.RPManagerService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RPManagerService(object):
    """存取RP 相關服務
    """

    @staticmethod
    def CheckRPRegistration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.RPManagerService/CheckRPRegistration',
            credentials__pb2.MsgRequest.SerializeToString,
            credentials__pb2.RPCheckReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class AuthenticationServiceStub(object):
    """FIDO 註冊及認證相關服務
    註冊 : client > username 
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterBegin = channel.unary_unary(
                '/credentials.AuthenticationService/RegisterBegin',
                request_serializer=credentials__pb2.MsgRequest.SerializeToString,
                response_deserializer=credentials__pb2.PublicKeyResponse.FromString,
                _registered_method=True)
        self.RegisterComplete = channel.unary_unary(
                '/credentials.AuthenticationService/RegisterComplete',
                request_serializer=credentials__pb2.JWTRequest.SerializeToString,
                response_deserializer=credentials__pb2.Message.FromString,
                _registered_method=True)
        self.LoginBegin = channel.unary_unary(
                '/credentials.AuthenticationService/LoginBegin',
                request_serializer=credentials__pb2.MsgRequest.SerializeToString,
                response_deserializer=credentials__pb2.JWTResponse.FromString,
                _registered_method=True)
        self.LoginComplete = channel.unary_unary(
                '/credentials.AuthenticationService/LoginComplete',
                request_serializer=credentials__pb2.JWTRequest.SerializeToString,
                response_deserializer=credentials__pb2.Message.FromString,
                _registered_method=True)


class AuthenticationServiceServicer(object):
    """FIDO 註冊及認證相關服務
    註冊 : client > username 
    """

    def RegisterBegin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterComplete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoginBegin(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoginComplete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthenticationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterBegin': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterBegin,
                    request_deserializer=credentials__pb2.MsgRequest.FromString,
                    response_serializer=credentials__pb2.PublicKeyResponse.SerializeToString,
            ),
            'RegisterComplete': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterComplete,
                    request_deserializer=credentials__pb2.JWTRequest.FromString,
                    response_serializer=credentials__pb2.Message.SerializeToString,
            ),
            'LoginBegin': grpc.unary_unary_rpc_method_handler(
                    servicer.LoginBegin,
                    request_deserializer=credentials__pb2.MsgRequest.FromString,
                    response_serializer=credentials__pb2.JWTResponse.SerializeToString,
            ),
            'LoginComplete': grpc.unary_unary_rpc_method_handler(
                    servicer.LoginComplete,
                    request_deserializer=credentials__pb2.JWTRequest.FromString,
                    response_serializer=credentials__pb2.Message.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'credentials.AuthenticationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('credentials.AuthenticationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AuthenticationService(object):
    """FIDO 註冊及認證相關服務
    註冊 : client > username 
    """

    @staticmethod
    def RegisterBegin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.AuthenticationService/RegisterBegin',
            credentials__pb2.MsgRequest.SerializeToString,
            credentials__pb2.PublicKeyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RegisterComplete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.AuthenticationService/RegisterComplete',
            credentials__pb2.JWTRequest.SerializeToString,
            credentials__pb2.Message.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def LoginBegin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.AuthenticationService/LoginBegin',
            credentials__pb2.MsgRequest.SerializeToString,
            credentials__pb2.JWTResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def LoginComplete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.AuthenticationService/LoginComplete',
            credentials__pb2.JWTRequest.SerializeToString,
            credentials__pb2.Message.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class grpctestServiceStub(object):
    """測試
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HelloWorld = channel.unary_unary(
                '/credentials.grpctestService/HelloWorld',
                request_serializer=credentials__pb2.HelloRequest.SerializeToString,
                response_deserializer=credentials__pb2.HelloResponse.FromString,
                _registered_method=True)


class grpctestServiceServicer(object):
    """測試
    """

    def HelloWorld(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_grpctestServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'HelloWorld': grpc.unary_unary_rpc_method_handler(
                    servicer.HelloWorld,
                    request_deserializer=credentials__pb2.HelloRequest.FromString,
                    response_serializer=credentials__pb2.HelloResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'credentials.grpctestService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('credentials.grpctestService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class grpctestService(object):
    """測試
    """

    @staticmethod
    def HelloWorld(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/credentials.grpctestService/HelloWorld',
            credentials__pb2.HelloRequest.SerializeToString,
            credentials__pb2.HelloResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
