import grpc
from gRPC import credentials_pb2
from gRPC import credentials_pb2_grpc
import json
from fido2.cose import ES256 



class RPManagerClient :
    def __init__(self, server_address):
        self.server_address = server_address
        
    # 檢查RP註冊
    def check_rp_registration(self, rp_name):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.RPManagerServiceStub(channel)
            request = credentials_pb2.MsgRequest(name=rp_name)
            response = stub.CheckRPRegistration(request)            
            return response

class AuthClient :
    def __init__(self, server_address):
        self.server_address = server_address
    
    # 進行註冊
    def register_begin(self , username):        
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.AuthenticationServiceStub(channel)            
            request = credentials_pb2.MsgRequest(name=username)
            response = stub.RegisterBegin(request)            
            return response
        
    def register_complete(self , token):
        print(token)
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.AuthenticationServiceStub(channel)
            request = credentials_pb2.JWTRequest(token=token)
            response = stub.RegisterComplete(request)
            return response
    # send ClientData
    def SendClientData(self , clientdata):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.AuthenticationServiceStub(channel)  
            
            data = credentials_pb2.CollectedClientData(
                challenge = clientdata.challenge,
                origin = clientdata.origin,
                type = clientdata.type,
                cross_origin = clientdata.cross_origin
            )
            response = stub.SendClientData(data)
            return response
    # send Attestation
    def SendAttestation(self, attestation , state ):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.AuthenticationServiceStub(channel)
           
            # Helper function to convert an int to bytes
            def int_to_bytes(value):
                if isinstance(value, int):
                    if value >= 0:
                        return value.to_bytes((value.bit_length() + 7) // 8 or 1, byteorder='big')
                    else:
                        return (-value).to_bytes((-value).bit_length() // 8 + 1, byteorder='big')
                return value  # 如果已經是 bytes 類型，直接返回

            # Creating the AAGUID object
            aaguid = credentials_pb2.AAGUID(value=attestation.auth_data.credential_data.aaguid)

            # Creating the AttestedCredentialData object
            credential_data = credentials_pb2.AttestedCredentialData(
                aaguid=aaguid,
                credential_id=attestation.auth_data.credential_data.credential_id,
                public_key={k: (v if isinstance(v, bytes) else int_to_bytes(v)) for k, v in attestation.auth_data.credential_data.public_key.items()}
            )

            # Creating the AuthenticatorData object
            auth_data = credentials_pb2.AuthenticatorData(
                rp_id_hash=attestation.auth_data.rp_id_hash,
                flags=attestation.auth_data.flags,
                counter=attestation.auth_data.counter,
                credential_data=credential_data
            )

            # Handling the att_stmt field
            att_stmt = {}
            x5c = []
            for k, v in attestation.att_stmt.items():
                if k == 'x5c':
                    x5c = v  # 保持 x5c 為 list[bytes]
                else:
                    att_stmt[k] = int_to_bytes(v)
            
            # Creating the AttestationObject
            data = credentials_pb2.AttestationObject(
                fmt=attestation.fmt,
                auth_data=auth_data,
                att_stmt=att_stmt,
                x5c=x5c,
                token=state
            )

           
            response = stub.SendAttestationObject(data)
            return response
class CredentialClient : 
    def __init__(self, server_address):
        self.server_address = server_address
    
    # 傳送給server
    def send_credentials_to_server(self,user_id, credentials):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.CredentialServiceStub(channel)
           
            
            public_key = credentials_pb2.PublicKey(
                kty= credentials["public_key"][1],
                alg= int(credentials["public_key"][3]),
                crv= int(credentials["public_key"][-1]),
                x=credentials["public_key"][-2],
                y=credentials["public_key"][-3]
            )
            
            request = credentials_pb2.CredentialRequest(
                user_id=str(user_id),
                public_key=public_key,
                sign_count=credentials["sign_count"],
                transports=credentials["transports"],
                aaguid=credentials["aaguid"],
                credential_id=credentials["credential_id"]
            )
            
            response = stub.StoreCredential(request)
            print(response.message)
            
    # credential authentication
    def send_credentials_to_auth(self,user_id, credentials):
        
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.CredentialServiceStub(channel)      
            
            
                 
            public_key = credentials_pb2.PublicKey(
                kty= credentials["public_key"]['1'],
                alg= int(credentials["public_key"]['3']),
                crv= int(credentials["public_key"]['-1']),
                x=credentials["public_key"]['-2'],
                y=credentials["public_key"]['-3']
            )
            
            request = credentials_pb2.CredentialRequest(
                user_id=str(user_id),
                public_key=public_key,
                sign_count=credentials["sign_count"],
                transports=credentials["transports"],
                aaguid=credentials["aaguid"],
                credential_id=credentials["credential_id"]
            )
            
            response = stub.SendCredentialToAuth(request)
            print(response.message)
            return response.message