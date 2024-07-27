from flask import Flask, jsonify, request 
from fido2.server import Fido2Server
from fido2.webauthn import CollectedClientData , AttestationObject , AttestedCredentialData , AuthenticatorData
from enum import Enum
import logging
import base64
import json
import jwt
from datetime import datetime , timedelta , timezone

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 日誌紀錄器
logging.basicConfig(level=logging.INFO)

# 建立一個根路由
@app.route('/')
def home():
    return "Hello, Flask???"


server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="direct")

uv = "discouraged"
global_state = {}

# 自定義JSON 序列化器
def custom_serializer(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Type {type(obj)} not serializable")

# 生成JWT
def generate_token(state):
    payload = {
        'state': state , 
        'exp' : datetime.now(tz=timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload , app.secret_key , algorithm='HS256')
    return token 

def verify_token(token):
    try :
        payload = jwt.decode(token , app.secret_key, algorithms=['HS256'])
        return payload['state']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidAudienceError:
        return None 

# POST 請求 註冊begin 
@app.route('/register/begin', methods=['POST'])
def post_data():
    index = 0
    posted_data  = request.get_json()
    username = posted_data["username"]
    user = {"id" : str(index).encode("utf-8") , "name" : username }
    index = index + 1 
    create_options, state = server.register_begin(
        user ,
        resident_key_requirement="required",
        user_verification=uv,
        authenticator_attachment="cross-platform",
    )
    app.logger.info("Statue is : %s" , state )
    token = generate_token(state) 
    
    public_key_json = json.dumps(create_options["publicKey"], default=custom_serializer, indent=4)
    
    data = {
        'message': 'success!',
        'public_key': public_key_json,
        'token' : token 
    }
    app.logger.info('Request Data : ' , data )
    return jsonify(data)

# POST 請求 註冊 complete
@app.route('/register/complete', methods=['POST'])
def post_complete_data():
    posted_data  = request.get_json()

    client_data = posted_data["client_data"]
    # app.logger.info('Client_data： %s',client_data)
    attestation_object  = posted_data["attestation_object"]
    app.logger.info('Attestation_object : %s' , attestation_object )   
    token = posted_data['token']
    # app.logger.info("Token: %s" , posted_data['token'] )
    state = verify_token(token)
   
    client_data = CollectedClientData.create(
        client_data['type'],
        base64.urlsafe_b64decode(client_data['challenge']),
        client_data['origin'],
        client_data['cross_origin'] == 'True'
    )
    
    credential_data = AttestedCredentialData.create(
        aaguid = base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['aaguid']),
        credential_id = base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['credential_id']),
        public_key = {
            1 : base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['public_key']['1']),
            3 :  base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['public_key']['3']),
            -2 : base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['public_key']['-2']),
            -1 : base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['public_key']['-1']),
            -3 : base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['public_key']['-3']),           
        }
    )
   
    
    auth_data = AuthenticatorData.create(
        base64.urlsafe_b64decode(attestation_object['auth_data']['rp_id_hash']),
        attestation_object['auth_data']['flags'],
        attestation_object['auth_data']['counter'],
        credential_data
    )
    
    attestation_object = AttestationObject.create(
        attestation_object['fmt'],
        auth_data,
        {
            'sig' : base64.urlsafe_b64decode(attestation_object['att_stmt']['sig']), 
            'alg' : base64.urlsafe_b64decode(attestation_object['att_stmt']['alg']),
            'x5c' : [base64.b64decode(cert) for cert in attestation_object['x5c']]
        }
    )
    auth_data = server.register_complete(state , client_data , attestation_object) 
    app.logger.info("Auth_data : %s" , auth_data.credential_data )
    data = {
        'message': 'success!',
        'data': auth_data.credential_data 
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
