from flask import Flask, jsonify, request , render_template, redirect , url_for , Blueprint , make_response
from fido2.server import Fido2Server
from dotenv import load_dotenv
from fido2.webauthn import CollectedClientData , AttestationObject , AttestedCredentialData , AuthenticatorData,Aaguid , PublicKeyCredentialDescriptor, CoseKey
import fido2.cbor as cbor
import struct
from transfer import credential_descriptor_transfer ,credential_descriptor_transfer_2
from enum import Enum
import base64
import json
import jwt
import os
import log_config
import secrets
from datetime import datetime , timedelta , timezone
import mysql.connector
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature as _InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ec import SECP256R1, EllipticCurvePublicNumbers
from cryptography.hazmat.primitives.asymmetric import ec

logger = log_config.logger

db_config = {
    'user': 'user',
    'password': 'password',
    'host': 'fido2_db',
    'database': 'fido2',
    'raise_on_warnings': True
}

webbp = Blueprint('web_routes', __name__)
webbp.secret_key = 'Jf9l1Kz3t5qDs8oG6jP7U3v0XwS9b4CkNzLmQxVc7rTfYnHaUv'

load_dotenv()

db_config = {
    'user': 'user',
    'password': 'password',
    'host': 'fido2_db',
    'database': 'fido2',
    'raise_on_warnings': True
}

# 解析 Base64 編碼的資料並轉換為二進制格式
def decode_base64_to_bytes(base64_string):
    try:
        return base64.b64decode(base64_string)
    except Exception as e:
        logger.error(f"Base64 解碼失敗: {str(e)}")
        return None
    
# 自定義JSON 序列化器
def custom_serializer(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Type {type(obj)} not serializable")

def serialize_bytes(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')  # 將字節數據轉換為 base64 編碼的字符串
    if isinstance(obj, dict):
        return {k: serialize_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize_bytes(v) for v in obj]
    return obj

# 生成JWT
def generate_token(state , username):
    payload = {
        'state': state ,
        'exp' : datetime.now(tz=timezone.utc) + timedelta(hours=1),
        'user' : username
    }
    token = jwt.encode(payload , webbp.secret_key , algorithm='HS256')
    return token

def verify_token(token):
    try :
        payload = jwt.decode(token , webbp.secret_key, algorithms=['HS256'])        
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidAudienceError:
        return None
    


server = Fido2Server({"id": "ag.yuntech.poc.com", "name": "Example RP"}, attestation="direct")
uv = "discouraged"
global_state = {}


#POST 請求 註冊 begin
@webbp.route('/web/register/begin', methods=['POST'])
def web_post_data():
    index = 0
    posted_data  = request.get_json()
    username = posted_data["username"]
    logger.info("Statue is : %s" , username )
    user_id_bytes = secrets.token_bytes(32)   
    
    user = {"id" : user_id_bytes , "name" : username }
    index = index + 1
    create_options, state = server.register_begin(
            user ,
            resident_key_requirement="required",
            user_verification=uv,
            authenticator_attachment="cross-platform",
    )
    logger.info("Statue is : %s" , state )
    token = generate_token(state, username)

    public_key_json = json.dumps(create_options["publicKey"], default=custom_serializer, indent=4)

    data = {
        'message': 'success!',
        'public_key': public_key_json,
        'token' : token
    }
    logger.info('Request Data :  %s' , data )
    return jsonify(data)    

# POST 請求 註冊 complete
@webbp.route('/web/register/complete', methods=['POST'])
def web_post_complete_data():

        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()
        
        # 解析請求中的資料
        res = request.get_json()
        
        data = res.get('token')
        logger.info("收到的數據: %s", data)
        # 解析 JWT token
        res= verify_token(data)
        logger.info("解析後的數據: %s", res)
        
        
        
        client_data_b64 = res['client_data']        
        client_data = json.loads(decode_base64_to_bytes(client_data_b64).decode('utf-8'))
        logger.info("client_data: %s", client_data)
        
        client_data =  CollectedClientData.create(
            client_data['type'],
            client_data['challenge'],
            client_data['origin'],
            client_data['crossOrigin'] == 'True'
        )
        
       
        attestation_object_b64 = res['attestation_object']
        
        attestation_object = decode_base64_to_bytes(attestation_object_b64)
        
        decode_data = cbor.decode(attestation_object)
        logger.info("attestation_object: %s", decode_data)
        authData = decode_data['authData']
        
        logger.info("authData: %s", authData)
        # AAGUID
        aaguid_bytes = authData[37:53]
        
        id_len_bytes = authData[53:55] # 取出第 53 到 55 位的資料
        credential_id_length = struct.unpack('>H', id_len_bytes)[0]  # '>H' 表示大端序的 16 位元無符號整數
        # 取得 credential ID
        credential_id = authData[55: 55 + credential_id_length]
        
        # 取得 public key bytes
        public_key_bytes = authData[55 + credential_id_length:]
        
        # 將 public key bytes 解碼為 CBOR 格式的物件
        public_key_object = cbor.decode(public_key_bytes)
        public_key = CoseKey.parse(public_key_object)
        logger.info("public_key: %s", public_key)
        credential_data = AttestedCredentialData.create(
            aaguid = aaguid_bytes,
            credential_id = credential_id,
            public_key = public_key
        )      
        
        rp_id_hash = authData[:32]  # 前 32 字節是 rp_id_hash
        flags = authData[32]  # 接下來的 1 字節是 flags
        sign_count = struct.unpack('>I', authData[33:37])[0]  # 接下來的 4 字節是 counter (大端序)
        
        auth_data = AuthenticatorData.create(
            rp_id_hash,
            flags,
            sign_count,
            credential_data
        )
        
        
        attestation_object = AttestationObject.create(
            decode_data["fmt"],
            auth_data,
            {
                'sig' : decode_data['attStmt']['sig'],
                'alg' : decode_data['attStmt']['alg'],
                'x5c' : decode_data['attStmt']['x5c']
            }
        )
        # 註冊完成?
        
        verify = verify_token(res['token'])
        state = verify['state']
        username = verify['user']
        
        auth_data = server.register_complete(state , client_data , attestation_object)
       
        
        
        logger.info("Auth_data : %s" , auth_data.credential_data)
        aaguid = str(auth_data.credential_data.aaguid)
        
        # 查詢是否有此username、如果沒有新增
        CHECKUSER = ("SELECT COUNT(*) FROM users WHERE username = %s " )
        cursor.execute(CHECKUSER,(username,))
        (count , ) = cursor.fetchone()
        if count == 0 :
            INSERT_USER = ("INSERT INTO users (username, email) VALUES ( %s , %s )")
            cursor.execute(INSERT_USER, (username,'example@gmail.com',))
            cnx.commit()
            logger.info("Inserted new users.")
        else :
            data = {
                'message' : 'Failed',
                'data' : '使用者已被註冊'
            }
            logger.error("使用者已被註冊")
            return make_response(jsonify(data), 409)
        
        # 查詢AAGUID是否已存在，如果沒有新增
        CHECK_CREDENTIAL = ('SELECT COUNT(*) FROM credentialData where aaguid = %s and username = %s')
        cursor.execute(CHECK_CREDENTIAL , (aaguid , username , ))
        (count , ) = cursor.fetchone()
        
        if count == 0 :
            public_key_dict = {k: base64.b64encode(v).decode('utf-8') if isinstance(v, bytes) else v for k, v in auth_data.credential_data.public_key.items()}
            public_keys = json.dumps(public_key_dict)
            ADD_CREDENTIAL = ("INSERT INTO credentialData (aaguid , credential_id , public_key,username) VALUES (%s , %s ,%s , %s )")    
            cursor.execute(ADD_CREDENTIAL , (aaguid, base64.b64encode(auth_data.credential_data.credential_id).decode("utf-8") , public_keys , username))
            cnx.commit()    
            logger.info("Inserted new credential data.")

            data = {
                'message': 'Success',
                'data': "Register Success "
            }
            return jsonify(data)
        else :
            data = {
                'message' : 'Failed',
                'data' : '使用者已被註冊'
            }
            logger.error("使用者已被註冊")
            return make_response(jsonify(data), 409)


    
# POST 請求 登入begin
@webbp.route('/web/login/begin', methods=['POST'])
def login_begin():
     # 獲取使用者名稱
    username = request.get_json()["username"]
    logger.info("Username: %s", username)
    

    

    # 從環境變數中獲取密鑰
    #agent_secret_key = os.getenv("Jf9l1Kz3t5qDs8oG6jP7U3v0XwS9b4CkNzLmQxVc7rTfYnHaUv")
    
    # 從資料庫中獲取憑證描述符
    credential_descriptor = credential_descriptor_transfer(webbp, username)  # 定義於其他模塊
    logger.debug("從資料庫取出的資料 %s" , credential_descriptor)
    # 開始 WebAuthn 驗證
    request_options, state = server.authenticate_begin(
        [credential_descriptor], 
        user_verification=uv
    )
    logger.info("STATE: %s", state)

    # 處理允許的憑證
    types_list = [cred["type"].value for cred in request_options["publicKey"]["allowCredentials"]]
    id_list = [base64.b64encode(cred["id"]).decode('utf-8') for cred in request_options["publicKey"]["allowCredentials"]]
    transports_list = [
        [transport.value for transport in cred["transports"]]
        for cred in request_options["publicKey"]["allowCredentials"]
    ]

    # 構建公鑰選項
    public_key = {
        'challenge': base64.b64encode(request_options["publicKey"]["challenge"]).decode('utf-8'),
        'rpId': request_options["publicKey"]["rpId"],
        'allowCredentials': [
            {
                'type': types_list,
                'id': id_list,
                'transports': transports_list
            }
        ],
        'userVerification': request_options["publicKey"]["userVerification"]
    }

    # 構建 payload 並生成 JWT
    payload = {
        "public_key": public_key,
        "token": state
    }
    logger.info('Payload: %s', payload)

    # 加密生成 JWT Token
    # data = jwt.encode(payload, agent_secret_key, algorithm='HS256')
    # logger.info('JWT Data: %s', data)

    # 回傳成功訊息
    response = {
        'message': 'success!',
        'data': payload
    }
    return jsonify(response), 200


# POST 請求 登入 complete
@webbp.route('/web/login/complete', methods=['POST'])
def login_complete():
    posted_data  = request.get_json()
    logger.info("Receive data  : %s" , posted_data) 
    # agent_secret_key = os.getenv("AGENT_SECRET_KEY")
    
    
    
    
    client_data = json.loads(base64.b64decode(posted_data['response']['clientDataJSON']))
    logger.info("client_data : %s " , client_data)
    
    client_data = CollectedClientData.create(
        client_data['type'],
        client_data['challenge'],
        client_data['origin'],
        client_data['crossOrigin'] == True 
    )
    
    credentials = credential_descriptor_transfer_2(webbp ,posted_data["username"] )
    authenticatorData = base64.b64decode(posted_data['response']['authenticatorData'])
    
    rp_id_hash = authenticatorData[:32]
    flags = authenticatorData[32] 
    counter = struct.unpack('>I', authenticatorData[33:37])[0]
    
    auth_data = AuthenticatorData.create(
        rp_id_hash ,
        flags,
        counter
    )
    
    signature = base64.b64decode(posted_data['response']['signature'])
    
    credential_id = base64.b64decode(posted_data['credential_id'])
    
    logger.info("credentials: %s" , credentials )

    res = server.authenticate_complete(
        posted_data['state'] , 
        [credentials],
        credential_id,
        client_data,
        auth_data,
        signature
    )


    logger.info("Res : %s" , res)
    data = {
        'message': 'success!'  ,
        'data' : '登入成功!'
    }
    return jsonify(data) ,200 
