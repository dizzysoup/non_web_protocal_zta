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

#測試
class grpctestServiceServicer(credentials_pb2_grpc.grpctestServiceServicer):
    def HelloWorld(self, request, context):
        username = request.username
        print(f"Received username: {username}")
        
        # 發送資料給 PDP
        status_code, response_text = self.send_to_pdp(username)
        
        final_reply = f"Response from PEP: received\nResponse from PDP: {response_text}"
        return credentials_pb2.HelloResponse(reply=final_reply)

    def send_to_pdp(self, username):
        url = "http://192.168.50.76:3000/users"
        data = {"username": username}
        try:
            response = requests.post(url, json=data)
            return response.status_code, response.text
        except requests.exceptions.RequestException as e:
            return None, str(e)


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
    
    def RegisterComplete(self , request , context):
        token = request.token
        
        
        url = "http://de.yunpoc.edu.tw:3000/fido2/register/complete"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "token" : token
        }
        print(payload)
        message = requests.post(url, json = payload, headers=headers).json()
        print(message)
        
        
        return credentials_pb2.Message(msg=message['data'])
    
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
    
    
    
def start_gGPC_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    credentials_pb2_grpc.add_CredentialServiceServicer_to_server(CredentialServiceServicer(), server)
    credentials_pb2_grpc.add_RPManagerServiceServicer_to_server(RPManagerService(), server)
    credentials_pb2_grpc.add_grpctestServiceServicer_to_server(grpctestServiceServicer(), server)
    credentials_pb2_grpc.add_AuthenticationServiceServicer_to_server(AuthenticationService() , server)
    server.add_insecure_port('[::]:50051')
    logger.debug("gRPC Server started on port 50051")
    server.start()
    print('Server started on port 50051.')
    server.wait_for_termination()




