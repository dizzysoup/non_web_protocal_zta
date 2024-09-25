from flask import Flask, jsonify, request , render_template, redirect , url_for
from fido2.server import Fido2Server
from dotenv import load_dotenv
from agent import bp 
from web import webbp
import fido2.cbor as cbor
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

logger = log_config.logger

app = Flask(__name__)
app.secret_key = 'supersecretkey'
load_dotenv()

db_config = {
    'user': 'user',
    'password': 'password',
    'host': 'fido2_db',
    'database': 'fido2',
    'raise_on_warnings': True
}

# 建立一個根路由
@app.route('/')
def home():
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor(dictionary=True)
    
    query = "SELECT *FROM credentialData" 
    cursor.execute(query)
    credentials = cursor.fetchall()
    
    query = cursor.execute("SELECT * FROM users ")
    users = cursor.fetchall()
    
    cursor.close()
    cnx.close()
    
    return render_template('credentials.html', credentials=credentials, users=users)

def serialize_bytes(obj):
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')  # 將字節數據轉換為 base64 編碼的字符串
    if isinstance(obj, dict):
        return {k: serialize_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize_bytes(v) for v in obj]
    return obj

@app.route('/delete_user/<string:user_name>', methods=['POST'])
def delete_user(user_name):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()   
    sql = "DELETE FROM users where username = %s"
    cursor.execute(sql,(user_name,))
    cnx.commit()
    
    cursor.close()
    cnx.close()
    return redirect("https://de.yuntech.poc.com:3443/")


@app.route('/delete/<credential_id>', methods=['POST'])
def delete_credential(credential_id):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    sql = "DELETE * FROM credentialData where aaguid = %s"
    cursor.execute(sql,(credential_id,))
    
    return redirect("https://de.yuntech.poc.com:3443/")


app.register_blueprint(bp)
app.register_blueprint(webbp)

if __name__ == '__main__':
    context = ('cert/server.crt' , 'cert/server.key')
    app.run(debug=True, host='0.0.0.0', port=5443 , ssl_context=context)
