from concurrent import futures
import grpc
import credentials_pb2
import credentials_pb2_grpc
import requests
import json
import pymysql
import json
import log_config
import requests
import base64

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
    def __init__(self):
        self.clientdata = None
        self.attestationobject = None 
    
    def RegisterBegin(self , request , context):
        url = "http://de.yunpoc.edu.tw:3000/fido2/register/begin"
        payload = {
            "username" : request.name 
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = requests.post(url, data=json.dumps(payload), headers=headers).json()        
        public_key_data = json.loads(data['public_key'])
        token = data['token']
        

        # 組織公鑰回傳格式
        response = credentials_pb2.PublicKeyResponse(
            attestation=public_key_data['attestation'],
            authenticatorSelection=credentials_pb2.AuthenticatorSelection(
                authenticatorAttachment=public_key_data['authenticatorSelection']['authenticatorAttachment'],
                requireResidentKey=public_key_data['authenticatorSelection']['requireResidentKey'],
                residentKey=public_key_data['authenticatorSelection']['residentKey'],
                userVerification=public_key_data['authenticatorSelection']['userVerification']
            ),
            challenge=public_key_data['challenge'],
            rp=credentials_pb2.RP(
                id=public_key_data['rp']['id'],
                name=public_key_data['rp']['name']
            ),
            user=credentials_pb2.User(
                id=public_key_data['user']['id'],
                name=public_key_data['user']['name']
            ),
            token = token
        )
        
        for param in public_key_data['pubKeyCredParams']:
            response.pubKeyCredParams.add(alg=param['alg'], type=param['type'])
       
        return response
    def SendClientData(self , request , context):
        self.clientdata = request
        return credentials_pb2.Message(msg=" client data stored success")
    
    def SendAttestationObject(self , request , context):
        url = "http://de.yunpoc.edu.tw:3000/fido2/register/complete"
        self.attestationobject = request
        
        client_data_dict = {
            "type": self.clientdata.type,
            "challenge": base64.b64encode(self.clientdata.challenge).decode('utf-8'),
            "origin": self.clientdata.origin,
            "cross_origin": "False"
        }
        
        credential_data_dict = {
            "aaguid": base64.b64encode(request.auth_data.credential_data.aaguid.value).decode('utf-8'),
            "credential_id": base64.b64encode(request.auth_data.credential_data.credential_id).decode('utf-8'),
            "public_key": {str(k): base64.b64encode(v).decode('utf-8') if isinstance(v, bytes) else v for k, v in request.auth_data.credential_data.public_key.items()}
        }
        
        auth_data_dict = {
            "rp_id_hash": base64.b64encode(request.auth_data.rp_id_hash).decode('utf-8'),
            "flags": request.auth_data.flags,
            "counter": request.auth_data.counter,
            "credential_data": credential_data_dict
        }
        
        att_stmt_dict = {k: base64.b64encode(v).decode('utf-8') if isinstance(v, bytes) else v for k, v in request.att_stmt.items()}

        attestation_object_dict = {
            "fmt": request.fmt,
            "auth_data": auth_data_dict,
            "att_stmt": att_stmt_dict,
            "x5c": [base64.b64encode(x).decode('utf-8') for x in request.x5c]
        }
        
        
        payload = {
               "client_data": client_data_dict,
               "attestation_object": attestation_object_dict,
               "token" : request.token
        }
        print(payload)
        headers = {
            "Content-Type": "application/json"
        }
        
        message = requests.post(url, data= json.dumps(payload), headers=headers).json()
        print(message)
        return credentials_pb2.Message(msg=" Received attestation object stored success")
    
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


