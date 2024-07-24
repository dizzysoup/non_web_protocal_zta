from concurrent import futures
import grpc
import credentials_pb2
import credentials_pb2_grpc
import requests
import json
import pymysql
import json
import log_config

logger = log_config.logger

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "web",
    "password": "password",
    "db": "PROXYDB",
    "charset": "utf8"
}

class CredentialServiceServicer(credentials_pb2_grpc.CredentialServiceServicer):
    def StoreCredential(self, request, context):
        user_id = request.user_id
        credentials = {
            "user_id": user_id,
            "public_key": {
                "kty": request.public_key.kty,
                "alg": request.public_key.alg,
                "crv": request.public_key.crv,
                "x": request.public_key.x,
                "y": request.public_key.y,
            },
            "sign_count": request.sign_count,
            "transports": request.transports,
            "aaguid": request.aaguid,
            "credential_id": request.credential_id
        }
        print(f"Received credentials for user_id {user_id}: {credentials}")
        # 在這裡儲存憑證
        self.store_credential_files(user_id, credentials)
        logger.info("使用者 user 註冊成功")
        return credentials_pb2.CredentialResponse(message="Credentials stored successfully")
    
    def store_credential_files(self, user_id, credentials):
        
        # 這裡是儲存憑證的邏輯        
        pass
    
    # 送憑證給pep， 進行驗證
    def SendCredentialToAuth(self, request , context ):
        user_id = request.user_id
        credentials = {
            "user_id": user_id,
            "public_key": {
                "kty": request.public_key.kty,
                "alg": request.public_key.alg,
                "crv": request.public_key.crv,
                "x": request.public_key.x,
                "y": request.public_key.y,
            },
            "sign_count": request.sign_count,
            "transports": request.transports,
            "aaguid": request.aaguid,
            "credential_id": request.credential_id
        }
        print(f"Received credentials for user_id {user_id}: {credentials}")
        # 在這裡驗證憑證
        self.Authchk(user_id, credentials)
        return credentials_pb2.CredentialResponse(message="Credentials Authentication successfully")
    
    def Authchk(self, user_id, credentials):
        logger.info("使用者user 登入成功")
        
        pass
    def Logout(self, request , context):
        data = {'expire': -1}
        with open('chk.json', 'w') as f :
            json.dump(data , f , indent=4)
        return credentials_pb2.CredentialResponse(message="Logout successfully")
    
class RPManagerService(credentials_pb2_grpc.RPManagerService):
    def CheckRPRegistration(self , request , context):
        conn = pymysql.connect(**db_settings)
        print(request.name)
        with conn.cursor() as cursor:
            command = "SELECT COUNT(*)  FROM proxy_hosts where Source = %s or Destination = %s "
            cursor.execute(command,(request.name, request.name))
            result = cursor.fetchall()[0][0]            
            print(result)
            conn.commit()       
            
        if result == 1 :
            data =  {
                "host" : request.name,
                "ip" : "192.168.71.4"
            }
            
            with open('chk.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            return credentials_pb2.RPCheckReply(is_registered = True, message = "資料存在" )
        else :
            return credentials_pb2.RPCheckReply(is_registered = False , message = "此IP或域名不儲存於AG中") 


class AuthenticationService(credentials_pb2_grpc.AuthenticationService):
    def RegisterBegin(self , request , context):
        username = request.name
        print(username)
        return credentials_pb2.MsgResponse(name = "success")
    
def start_gGPC_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    credentials_pb2_grpc.add_CredentialServiceServicer_to_server(CredentialServiceServicer(), server)
    credentials_pb2_grpc.add_RPManagerServiceServicer_to_server(RPManagerService(), server)
    credentials_pb2_grpc.add_AuthenticationServiceServicer_to_server(AuthenticationService() , server)
    server.add_insecure_port('[::]:50051')
    logger.debug("gRPC Server started on port 50051")
    server.start()
    print('Server started on port 50051.')
    server.wait_for_termination()


