function goBack() {
    window.location.href = 'index.html';
}

// Base64 to ArrayBuffer
function base64ToArrayBuffer(base64) {
    if (typeof base64 !== 'string' || base64.trim() === '') {
    console.error('無效的 Base64 字串:', base64);
    return null;
 }

    // 檢查字串長度是否是4的倍數，否則補齊'='
    while (base64.length % 4 !== 0) {
        base64 += '=';
    }

    try {
        const binaryString = window.atob(base64); // 嘗試解碼
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        return bytes.buffer;
    } catch (e) {
        console.error("解碼失敗:", e);
        return null;  // 或者返回一個預設值
    }
}

// 將 ArrayBuffer 轉為 Base64 字串
function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    bytes.forEach((b) => binary += String.fromCharCode(b));
    return window.btoa(binary);
}

function prepareCredentialForServer(credential, token) {
    console.log(credential.response.attestationObject);
    console.log(arrayBufferToBase64(credential.response.attestationObject))
    return {
      id: credential.id,
      rawId: arrayBufferToBase64(credential.rawId),
      type: credential.type,
      client_data: arrayBufferToBase64(credential.response.clientDataJSON),
      attestation_object: arrayBufferToBase64(credential.response.attestationObject),
      token : token 
    };
  }
async function registerUser() {
    var username = $("#username").val();            

    if (username === "" ) {
        alert("Please enter username");
        return;
    }

    // 開始註冊，發送 POST 請求獲取 challenge
    const response = await fetch("/register/begin", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username })
    }).catch(e => {
        console.error(e)
    });
   
    const result = await response.json();

    let publicKeyObj;
    try {
        publicKeyObj = JSON.parse(result.public_key);
        
    } catch (error) {
        console.error("無法解析 public_key:", error);
        alert("後端返回的資料格式錯誤");
        return;
    }

   // 確保 challenge 存在並轉換為 ArrayBuffer
    const challenge = publicKeyObj.challenge;
   

    if (!challenge) {
        console.error("無效的 challenge:", challenge);
        alert("後端返回的 challenge 資料錯誤");
        return;
    }

    // 轉換 challenge 為 ArrayBuffer
    const challengeArrayBuffer = base64ToArrayBuffer(challenge);
    if (!challengeArrayBuffer) {
        alert("無法轉換 challenge，請稍後再試");
        return;
    }
    
    const userID = publicKeyObj.user.id;
    const id = Uint8Array.from(window.atob(userID), c => c.charCodeAt(0));

    const publicKeyCredentialCreationOptions = {
        challenge: challengeArrayBuffer,
        rp: {
            name: "Tech Bridge"
        },
        user: {
            id,
            name:  username ,
            displayName: "Arvin",
        },
        pubKeyCredParams: [
            {
                type: "public-key",
                alg: -7   // ES256 (必須支持)
            },
            {
                type: "public-key",
                alg: -257 // RS256 (推薦支持)
            }
        ],
        authenticatorSelection: {
            authenticatorAttachment: "cross-platform",
        },
        timeout: 60000,
        attestation: "direct"
    };



    if (navigator.credentials && navigator.credentials.create) {
        try {
            // key 驅動
            const credential = await navigator.credentials.create({
                publicKey: publicKeyCredentialCreationOptions
            });
            
            const credentialJSON = prepareCredentialForServer(credential,result.token);
            console.log(credentialJSON)
           
            // 完成註冊，處理註冊完成後的邏輯
            // 可以在這裡發送 credential 資料到後端，進行註冊完成的驗證
            const completeResponse = await fetch("/register/complete", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "credential" :  credentialJSON}) // 將憑證資料發送到後端
            });

            if (completeResponse.status == 200) {               
                // window.location.href = "https://ag.yuntech.poc.com:8080/sshpage";
             } else {
                 alert("註冊失敗，請稍後再試");
             }
         } catch (error) {
             console.error("憑證創建失敗:", error);
             alert("註冊過程中出現錯誤，請稍後再試。");
         }
     } else {
         console.error("WebAuthn API not supported in this browser.");
         alert("您的瀏覽器不支援 WebAuthn API，請使用其他瀏覽器重試。");
     }
    }