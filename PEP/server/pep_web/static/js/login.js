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

//使用者登入
async function loginUser() {
    var username = $("#username").val();
    if (username === "") {
        alert("Please enter a username");
        return;
    }

    
    console.log('Username saved:', username); // 確認是否成功儲存

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
    try {
    const completeResponse = await fetch(url_logincomplete, {
        method: 'POST',
        headers: {
                'Content-Type': 'application/json',
                "Origin" : window.location.origin
        },
        body: JSON.stringify(respdata)
    });

    const result = await completeResponse.json();   
    if (completeResponse.ok && result.message === 'success!') {
            alert('登入成功！');
            const url = "https://de.yuntech.poc.com:3443/users/" + username ; 
            const response = await (await fetch(url)).json();
            
            console.log(response[0].id);
            localStorage.setItem('username', username); // 立即儲存 username
            localStorage.setItem('user_id', response[0].id); // 立即儲存 user id 
            // 登入成功後跳轉到 sshindex.html
            window.location.href = '/RemotePage/'; // 根據實際的路徑設定
    } else {
            alert('登入失敗，請重試');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('登入失敗');
    }

}
            
        
    



