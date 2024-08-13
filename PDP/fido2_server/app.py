from flask import Flask, jsonify, request , render_template
from fido2.server import Fido2Server
from dotenv import load_dotenv
from fido2.webauthn import CollectedClientData , AttestationObject , AttestedCredentialData , AuthenticatorData
from enum import Enum
import logging
import base64
import json
import jwt
import os
from datetime import datetime , timedelta , timezone
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = 'supersecretkey'
load_dotenv()

db_config = {
    'user': 'user',
    'password': 'password',
    'host': '172.18.0.3',
    'database': 'fido2',
    'raise_on_warnings': True
}

# 日誌紀錄器
logging.basicConfig(level=logging.INFO)

#測試
@app.route('/fido2test', methods=['POST'])
def handle_fido2_request():
    data = request.get_json()
    username = data.get('username')

    cnx = mysql.connector.connect(**db_config)

    if username:
        with cnx.cursor() as cursor:
            # 查詢用戶資料
            sql = "SELECT AAGUID, CredentialID, PublicKey FROM Users WHERE Username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()

        if result:
            # 返回用戶資料
            aaguid, credential_id, public_key = result
            user_data = {
                "AAGUID": aaguid,
                "CredentialID": credential_id,
                "PublicKey": public_key
            }
            print(f"FIDO2 伺服器檢索到使用者數據: {username}")
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Username is required"}), 400

# 建立一個根路由
@app.route('/')
def home():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(dictionary=True)
    
    query = "SELECT *FROM credentialData" 
    cursor.execute(query)
    credentials = cursor.fetchall()
    
    cursor.close()
    cnx.close()
    
    return render_template('credentials.html', credentials=credentials)
    
    
    


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
def generate_token(state , username):
    payload = {
        'state': state ,
        'exp' : datetime.now(tz=timezone.utc) + timedelta(hours=1),
        'user' : username
    }
    token = jwt.encode(payload , app.secret_key , algorithm='HS256')
    return token

def verify_token(token):
    try :
        payload = jwt.decode(token , app.secret_key, algorithms=['HS256'])
        return payload['state'], payload['user']
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
    token = generate_token(state, username)

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
    agent_secret_key = os.getenv("AGENT_SECRET_KEY")
    
    data = jwt.decode(posted_data["token"], agent_secret_key , algorithms=['HS256'])
    
    app.logger.info("Decode Token is %s" , data)
    
    client_data = data["client_data"]
    # app.logger.info('Client_data： %s',client_data)
    attestation_object  = data["attestation_object"]

    token = data['token']
    # app.logger.info("Token: %s" , posted_data['token'] )
    state , username = verify_token(token)
    app.logger.info('UserName : %s' , username )

    # checked user
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    CHECKUSER = ("SELECT COUNT(*) FROM users WHERE username = %s " )
    cursor.execute(CHECKUSER,(username,))
    (count , ) = cursor.fetchone()
    if count == 0 :
        INSERT_USER = ("INSERT INTO users (username, email) VALUES ( %s , %s )")
        cursor.execute(INSERT_USER, (username,'example@gmail.com',))
        cnx.commit()
        app.logger.info("Inserted new users.")
    

    client_data = CollectedClientData.create(
        client_data['type'],
        base64.urlsafe_b64decode(client_data['challenge']),
        client_data['origin'],
        client_data['cross_origin'] == 'True'
    )
    public_key = attestation_object['auth_data']['credential_data']['public_key']
   
    public_key = {
            1: base64.urlsafe_b64decode(public_key.get('1')) if isinstance(public_key.get('1'), str) else public_key.get('1'),
            3: base64.urlsafe_b64decode(public_key.get('3')) if isinstance(public_key.get('3'), str) else public_key.get('3'),
            -1 : base64.urlsafe_b64decode(public_key.get('-1')) if isinstance(public_key.get('-1'), str) else public_key.get('-1'),
            -2 : base64.urlsafe_b64decode(public_key.get('-2')) if isinstance(public_key.get('1'), str) else public_key.get('-2'),
            -3 : base64.urlsafe_b64decode(public_key.get('-3')) if isinstance(public_key.get('-3'), str) else public_key.get('-3'),
    } 
    
    
    
    credential_data = AttestedCredentialData.create(
        aaguid = base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['aaguid']),
        credential_id = base64.urlsafe_b64decode(attestation_object['auth_data']['credential_data']['credential_id']),
        public_key = {k: v for k, v in public_key.items() if v is not None}
    )


    auth_data = AuthenticatorData.create(
        base64.urlsafe_b64decode(attestation_object['auth_data']['rp_id_hash']),
        attestation_object['auth_data']['flags'],
        attestation_object['auth_data']['counter'],
        credential_data
    )
    att_stmt = attestation_object['att_stmt']
    
    attestation_object = AttestationObject.create(
        attestation_object['fmt'],
        auth_data,
        {
            'sig' : base64.urlsafe_b64decode(attestation_object['att_stmt']['sig']),
            'alg' : base64.urlsafe_b64decode(att_stmt.get('alg')) if isinstance(att_stmt.get('alg'), str) else att_stmt.get('alg'),
            'x5c' : base64.urlsafe_b64decode(att_stmt.get('x5c')) if isinstance(att_stmt.get('x5c'), str) else att_stmt.get('x5c')
        }
    )
   
    auth_data = server.register_complete(state , client_data , attestation_object)
    app.logger.info("Auth_data : %s" , auth_data.credential_data)
    aaguid = str(auth_data.credential_data.aaguid)
        
    CHECK_CREDENTIAL = ('SELECT COUNT(*) FROM credentialData where aaguid = %s and username = %s')
    cursor.execute(CHECK_CREDENTIAL , (aaguid , username , ))
    (count , ) = cursor.fetchone()
    
    if count == 0 :
        
        
        public_key_dict = {k: v.hex() if isinstance(v, bytes) else v for k, v in auth_data.credential_data.public_key.items()}
        public_keys = json.dumps(public_key_dict)
        app.logger.info("PublicKeys : %s" , public_keys)
        ADD_CREDENTIAL = ("INSERT INTO credentialData (aaguid , credential_id , public_key,username) VALUES (%s , %s ,%s , %s )")    
        cursor.execute(ADD_CREDENTIAL , (aaguid, auth_data.credential_data.credential_id.hex() , public_keys , username))
        cnx.commit()    
        app.logger.info("Inserted new credential data.")

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
        app.logger.error("使用者已被註冊")
        return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
