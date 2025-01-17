import base64
import json

# register begin 使用到的公鑰格式
def public_key_response_to_dict(response):
    return {
        "attestation": response.attestation,
        "authenticatorSelection": {
            "authenticatorAttachment": response.authenticatorSelection.authenticatorAttachment,
            "requireResidentKey": response.authenticatorSelection.requireResidentKey,
            "residentKey": response.authenticatorSelection.residentKey,
            "userVerification": response.authenticatorSelection.userVerification,
        },
        "challenge":  base64.urlsafe_b64decode(response.challenge),
        "pubKeyCredParams": [
            {"alg": param.alg, "type": param.type} for param in response.pubKeyCredParams
        ],
        "rp": {
            "id": response.rp.id,
            "name": response.rp.name,
        },
        "user": {
            "id": base64.b64decode(response.user.id),
            "name": response.user.name,            
        },
    }
    
    
def clientData_transfer(response):
    return {
        "type" : response.type,
        "challenge" :  base64.b64encode(response.challenge).decode('utf-8'),
        "origin" : response.origin,
        "cross_origin" : response.cross_origin
    }
    
def attestation_object_transfer(response):
    encoded_public_key = {
        k: base64.b64encode(v).decode('utf-8') if isinstance(v, bytes) else v
        for k, v in response.auth_data.credential_data.public_key.items()
    }
    
    encoded_att_stmt = {
        k: [base64.b64encode(cert).decode('utf-8') for cert in v] if k == 'x5c' else base64.b64encode(v).decode('utf-8') if isinstance(v, bytes) else v
        for k, v in response.att_stmt.items()
    }
    return {
        "fmt" : response.fmt,
        "auth_data": {
            "rp_id_hash": base64.b64encode(response.auth_data.rp_id_hash).decode('utf-8'),
            "flags": response.auth_data.flags,
            "counter": response.auth_data.counter,
            "credential_data": {
                "aaguid":  base64.b64encode(response.auth_data.credential_data.aaguid).decode('utf-8'),
                "credential_id": base64.b64encode(response.auth_data.credential_data.credential_id).decode('utf-8'),
                "public_key": encoded_public_key
            }
        },
        "att_stmt": encoded_att_stmt
        
    }
            
def authenticator_assertion_response_transfer(response):
    client_data = {
        "type": response.client_data.type,
        "challenge": base64.b64encode(response.client_data.challenge).decode('utf-8'),
        "origin": response.client_data.origin,
        "cross_origin": response.client_data.cross_origin
    }
    authenticator_data = {
        "rp_id_hash": base64.b64encode(response.authenticator_data.rp_id_hash).decode('utf-8'),
        "flags": response.authenticator_data.flags,
        "counter": response.authenticator_data.counter,
        "credential_data": None if response.authenticator_data.credential_data is None else base64.b64encode(response.authenticator_data.credential_data).decode('utf-8'),
        "extensions": response.authenticator_data.extensions
    }
    
    json_response = {
        "client_data": client_data,
        "authenticator_data": authenticator_data,
        "signature": base64.b64encode(response.signature).decode('utf-8'),
        "user_handle": None if response.user_handle is None else base64.b64encode(response.user_handle).decode('utf-8'),
        "credential_id": base64.b64encode(response.credential_id).decode('utf-8'),
        "extension_results": response.extension_results
    }
    
    return json_response