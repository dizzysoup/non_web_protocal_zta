import base64

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