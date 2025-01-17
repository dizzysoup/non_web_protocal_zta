import express from 'express';
import axios from 'axios';
import ldap from 'ldapjs';
import winlogger from '../components/log.js';
import https from 'https';
var router = express.Router();

const ldapOptions = {
  url: 'ldap://192.168.50.243', 
};


const bindDN = 'CN=Administrator,CN=Users,DC=yuntech,DC=poc,DC=com'; 
const bindPassword = '1qaz@WSX3edc'; 
const searchBase = 'DC=yuntech,DC=poc,DC=com'; 
winlogger.info(`Search base: ${searchBase}`);

// 獲取 IP 地址
function getClientIp(req) {
  return  req.socket.remoteAddress;
}
// 檢查 username 是否存在於 AD
function checkUsernameInAD(username, callback) {
  const client = ldap.createClient(ldapOptions);

  client.bind(bindDN, bindPassword, (err) => {
    if (err) {
      winlogger.error('Failed to bind LDAP: ' + err.message);
      return callback(err, null);
    } else {
      winlogger.info('LDAP bind successful');
      const clientIp = getClientIp(req);
      winlogger.info(`Request from IP: ${clientIp}, 發起登入請求`);
    }

    const searchFilter = `(sAMAccountName=${username})`;
    winlogger.info(`Search filter: ${searchFilter}`);

    client.search(searchBase, { filter: searchFilter, scope: 'sub', attributes: ['*'] }, (err, res) => {
      if (err) {
        return callback(err, null);
      }

      let userFound = false;

      res.on('searchEntry', (entry) => {
        winlogger.info('Entry found in AD: ' + JSON.stringify(entry.object, null, 2));
        userFound = true; // 找到用戶
      });

      res.on('end', () => {
        client.unbind();
        callback(null, userFound);
      });

      res.on('error', (err) => {
        client.unbind();
        callback(err, null);
      });
    });
  });
}

// 檢查 username 是否存在於AD
router.post('/check/ADuser', function(req, res, next) {
  const requestData = req.body;
  const username = requestData.username;

  // 獲取並記錄 IP 地址
  const clientIp = getClientIp(req);//
  winlogger.info(`Request from IP: ${clientIp}, Username: ${username}`);

  checkUsernameInAD(username, (err, exists) => {
    if (err) {
      return res.status(500).json({ status: 'error', error: 'AD query failed' });
    }

    if (!exists) {
      return res.status(404).json({ status: 'error', error: 'Username not found in AD' });
    }

    res.json({ status: 'success', message: 'Username exists in AD' });
  });
});


const httpsAgent = new https.Agent({
  rejectUnauthorized: false, // 忽略自簽名憑證錯誤
});


// 註冊流程
router.post('/register/begin', function(req, res, next) {

  winlogger.info("使用者發起註冊請求，重定向至Fido Server");
  const requestData = req.body;4
  winlogger.info("request data: " + JSON.stringify(requestData, null, 2));
  const username = requestData.username;

  

  // 首先檢查 username 是否存在於 AD 中
  checkUsernameInAD(username, (err, exists) => {
    if (err) {
      winlogger.error('Error checking username in AD: ' + err.message);
      return res.status(404).json({ status: 'error', error: 'AD query failed' });
    }

    if (!exists) {
      winlogger.info('Username does not exist in AD');
      return res.status(404).json({ status: 'error', error: 'Username not found in AD' });
    }

    // 如果 username 存在於 AD 中，繼續請求
    winlogger.info('Username exists in AD, proceeding to send request to Fido Server');

    axios.post('https://fido2_server:5443/agent/register/begin', requestData , {httpsAgent})
      .then(response => {
        winlogger.info("Fido Server 回傳 " + response.data);
        res.status(200).json(response.data);
      })
      .catch(error => {
        console.error(error.message);
        winlogger.error(error.message);
        res.status(404).json({ status: 'error', error: error.message });
      });
  });
});

router.post('/register/complete', function(req, res, next) {
    winlogger.info("使用者完成FIDO Key 指紋辨識，正在重定向至FIDO Server 進行註冊完成..")
    const requestData = req.body 
    axios.post('https://fido2_server:5443/agent/register/complete' , requestData , {httpsAgent})
      .then(res=> res.json())
      .then(response => {
        winlogger.info("註冊成功：" + response) ;
        res.json(response.data);
      })
      .catch(error => {
        winlogger.error("註冊失敗" + error.message);
        console.error(error.message);
        res.status(500).json({status: 'error' , error : error.message});
      })
});
// 登入流程
router.post('/login/begin', function(req, res, next) {
  // 獲取並記錄 IP 地址
  const clientIp = getClientIp(req);
  winlogger.info(`Request from IP: ${clientIp}, 發起登入請求`);//
  winlogger.info("使用者發起登入請求，重定向至Fido Server");
  const requestData = req.body
  winlogger.info("request data: " + JSON.stringify(requestData, null, 2));
  const username = requestData.username;
  
  // 首先檢查 username 是否存在於 AD 中
  checkUsernameInAD(username, (err, exists) => {
    if (err) {
      winlogger.error('Error checking username in AD: ' + err.message);
      return res.status(500).json({ status: 'error', error: 'AD query failed' });
    }

    if (!exists) {
      winlogger.info('Username does not exist in AD');
      return res.status(404).json({ status: 'error', error: 'Username not found in AD' });
    }

    // 如果 username 存在於 AD 中，繼續請求
    winlogger.info('Username exists in AD, proceeding to send request to Fido Server');

   // 使用 fetch 進行 POST 請求
   axios.post('https://fido2_server:5443/agent/login/begin', requestData, {
    headers: {
      'Content-Type': 'application/json',
    },
    httpsAgent: httpsAgent, // 使用 httpsAgent 設定
  })
    .then(response => {
      winlogger.info(" axios  URL  https://fido2_server:5443/agent/login/begin");
      winlogger.info(response.data); // 輸出接收到的資料
      res.status(200).json(response.data)
    })
    .catch(error => {
      winlogger.error('發送請求時發生錯誤:', error); // 錯誤處理
    
    });
});
});



router.post('/login/complete', function(req, res, next) {
  winlogger.info("使用者完成FIDO Key 指紋辨識，正在重定向至FIDO Server 進行登入驗證..?????????????????")
  const requestData = req.body 
  axios.post('https://fido2_server:5443/agent/login/complete' , requestData,{httpsAgent})    
    .then(response => {      
      winlogger.info(response.data) ;
      res.json(response.data);
    })
    .catch(error => {
      winlogger.error("登入失敗 : " + error.message);
      console.error("Error forward ");
      res.status(500).json({status: 'error' , error : error.message});
    })
    
});


export default router ; 
