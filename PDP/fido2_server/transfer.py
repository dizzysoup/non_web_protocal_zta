from fido2.webauthn import  AttestedCredentialData ,Aaguid , PublicKeyCredentialDescriptor
import mysql.connector
import json 

import base64



db_config = {
    'user': 'user',
    'password': 'password',
    'host': '172.18.0.3',
    'database': 'fido2',
    'raise_on_warnings': True
}

def credential_descriptor_transfer(app , username):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    
    CHECKUSER = ("SELECT credential_id,aaguid,public_key FROM credentialData WHERE username = %s " )
    cursor.execute(CHECKUSER,(username,))
    credentials = cursor.fetchall()
    
    credential_id, aaguid, public_key = credentials[0]  
    credential_id = str(credential_id)
    credential_id = credential_id[2:len(credential_id)-1]
    credential_id = base64.b64decode(str(credential_id))
    
    public_key = {
        int(k): (base64.b64decode(v) if isinstance(v, str) else v)
        for k , v in json.loads(public_key).items()
    }
    aaguid_bytes = bytes.fromhex(aaguid.replace('-',''))
    
    aattested_credential = AttestedCredentialData.create(Aaguid(aaguid_bytes), credential_id, public_key)
    credential_descriptor = PublicKeyCredentialDescriptor(
        type="public-key",
        id=aattested_credential.credential_id,
        transports=["usb"],
    )
    cursor.close()
    cnx.close()
    
    return credential_descriptor

def credential_descriptor_transfer_2(app , username):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    
    CHECKUSER = ("SELECT credential_id,aaguid,public_key FROM credentialData WHERE username = %s " )
    cursor.execute(CHECKUSER,(username,))
    credentials = cursor.fetchall()
    
    credential_id, aaguid, public_key = credentials[0]  
    
    credential_id = str(credential_id)
    credential_id = credential_id[2:len(credential_id)-1]
    credential_id = base64.b64decode(str(credential_id))
    public_key = {
        int(k): (base64.b64decode(v) if isinstance(v, str) else v)
        for k , v in json.loads(public_key).items()
    }
    aaguid_bytes = bytes.fromhex(aaguid.replace('-',''))
    app.logger.info(isinstance(credential_id , bytes))
    aattested_credential = AttestedCredentialData.create(Aaguid(aaguid_bytes), credential_id, public_key)

    cursor.close()
    cnx.close()
    
    return aattested_credential