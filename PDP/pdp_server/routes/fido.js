import express from 'express';
import axios from 'axios';
import ldap from 'ldapjs';
import winlogger from '../components/log.js';
var router = express.Router();

const ldapOptions = {
  url: 'ldap://192.168.50.243', 
};

const bindDN = 'CN=Administrator,CN=Users,DC=yuntech,DC=poc,DC=com'; 
const bindPassword = '1qaz@WSX3edc'; 
const searchBase = 'DC=yuntech,DC=poc,DC=com'; 
winlogger.info(`Search base: ${searchBase}`);

// 檢查 username 是否存在於 AD
function checkUsernameInAD(username, callback) {
  const client = ldap.createClient(ldapOptions);

  client.bind(bindDN, bindPassword, (err) => {
    if (err) {
      winlogger.error('Failed to bind LDAP: ' + err.message);
      return callback(err, null);
    } else {
      winlogger.info('LDAP bind successful');
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

// 註冊流程
router.post('/register/begin', function(req, res, next) {
  winlogger.info("使用者發起註冊請求，重定向至Fido Server");
  const requestData = req.body;
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

    axios.post('http://192.168.50.76:5000/register/begin', requestData)
      .then(response => {
        winlogger.info("Fido Server 回傳 " + response.data);
        res.json(response.data);
      })
      .catch(error => {
        console.error("Error forward ");
        winlogger.error(error.message);
        res.status(500).json({ status: 'error', error: error.message });
      });
  });
});

router.post('/register/complete', function(req, res, next) {
    winlogger.info("使用者完成FIDO Key 指紋辨識，正在重定向至FIDO Server 進行註冊完成..")
    const requestData = req.body 
   
    
    axios.post('http://192.168.50.76:5000/register/complete' , requestData)
      .then(response => {
        winlogger.info("註冊成功：" + response.data) ;
        res.json(response.data);
      })
      .catch(error => {
        winlogger.error("註冊失敗" + error.message);
        console.error("Error forward ");
        res.status(500).json({status: 'error' , error : error.message});
      })
});

router.post('/login/begin', function(req, res, next) {
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

  axios.post('http://192.168.50.76:5000/login/begin' , requestData)
    .then(response => {
      winlogger.info("Fido Server 回傳 " + response.data);
      res.status(200).json(response.data);
    })
    .catch(error => {
      winlogger.error(error.message);
      console.error("Error forward ");
      res.status(500).json({status: 'error' , error : error.message});
    })
});
});
router.post('/login/complete', function(req, res, next) {
  winlogger.info("使用者完成FIDO Key 指紋辨識，正在重定向至FIDO Server 進行登入驗證..")
  const requestData = req.body 
  axios.post('http://192.168.50.76:5000/login/complete' , requestData)
    .then(response => {
      winlogger.info("登入成功：" + response.data) ;
      res.json(response.data);
    })
    .catch(error => {
      winlogger.error("登入失敗" + error.message);
      console.error("Error forward ");
      res.status(500).json({status: 'error' , error : error.message});
    })
    
});


export default router ; 
