// Base64 to ArrayBuffer
function bufferDecode(value) {
    return Uint8Array.from(atob(value), c => c.charCodeAt(0));
}

function base64ToUint8Array(base64) {
    const binaryString = window.atob(base64); // 解碼 Base64 字串為二進位字串
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i); // 將每個字元轉換為對應的字節
    }
    return bytes;
}


// ArrayBuffer to Base64
function bufferEncode(value) {
    return btoa(String.fromCharCode.apply(null, new Uint8Array(value)))
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=/g, "");
}

function arrayBufferToBase64(buffer) {
    // 將 ArrayBuffer 轉換為 Uint8Array
    const bytes = new Uint8Array(buffer);
    let binary = '';
    
    // 將每個 byte 轉換為對應的字元
    bytes.forEach((b) => binary += String.fromCharCode(b));
    
    // 使用 btoa() 進行 Base64 編碼
    return window.btoa(binary);
}

// 登入
const url_loginbegin = 'https://de.yuntech.poc.com:3443/webfido/login/begin';
const url_logincomplete =  'https://de.yuntech.poc.com:3443/webfido/login/complete';


async function loginUser() {
    var username = $("#username").val();
    if (username === "") {
        alert("Please enter a username");
        return;
    }
    const response = await fetch(url_loginbegin,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body: JSON.stringify({ username })
        });

    if(response.status != 200 ){
            alert("登入流程失敗");
            return;
    }

    const options = await response.json();
    const publicKey = options.data.public_key;
    console.log(options.data)

    const credentialIdUint8Array = base64ToUint8Array(publicKey.allowCredentials[0].id);

    const publicKeyCredentialRequestOptions = {
            challenge: base64ToUint8Array(publicKey.challenge),
            allowCredentials: [{
                id: credentialIdUint8Array,
                type: 'public-key',
                transports: ['usb', 'ble', 'nfc'],
            }],
            timeout: 60000,
    }

    // 驅動fido     
    const assertion = await navigator.credentials.get({
            publicKey: publicKeyCredentialRequestOptions
    });
    console.log("--------------------------------")
    console.log(assertion)

    const respdata = {
            id: assertion.id,
            rawId: arrayBufferToBase64(assertion.rawId),
            credential_id : publicKey.allowCredentials[0].id[0] , 
            response: {
                clientDataJSON: arrayBufferToBase64(assertion.response.clientDataJSON),
                authenticatorData: arrayBufferToBase64(assertion.response.authenticatorData),
                signature: arrayBufferToBase64(assertion.response.signature),
                userHandle: arrayBufferToBase64(assertion.response.userHandle)
            },
            type: assertion.type,
            username: username , 
            state: options.data.token
    }
    console.log( window.location.origin)
    const completeResponse = await fetch(url_logincomplete, {
        method: 'POST',
        headers: {
                'Content-Type': 'application/json',
                "Origin" : window.location.origin
        },
        body: JSON.stringify(respdata)
    });

    if (!completeResponse.ok) {
                throw new Error('登入失敗');
    }else 
        alert('登入成功！');
}

            
        
    



