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
    # 註冊完成
    def register_complete(self , token):       
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.AuthenticationServiceStub(channel)
            request = credentials_pb2.JWTRequest(token=token)
            response = stub.RegisterComplete(request)
            return response
    # 進行登入
    def login_begin(self , username):        
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.AuthenticationServiceStub(channel)            
            request = credentials_pb2.MsgRequest(name=username)
            response = stub.LoginBegin(request)            
            return response
    # 登入完成
    def login_complete(self , token):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = credentials_pb2_grpc.AuthenticationServiceStub(channel)
            request = credentials_pb2.JWTRequest(token=token)
            response = stub.LoginComplete(request)
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