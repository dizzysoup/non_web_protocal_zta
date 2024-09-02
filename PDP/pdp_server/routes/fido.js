import express from 'express';
import axios from 'axios';
import winlogger from '../components/log.js';
var router = express.Router();


router.post('/register/begin', function(req, res, next) {
    winlogger.info("使用者發起註冊請求，重定向至Fido Server");
    const requestData = req.body 

    axios.post('http://192.168.50.76:5000/register/begin' , requestData)
      .then(response => {
        winlogger.info("Fido Server 回傳 " + response.data);
        res.json(response.data);
      })
      .catch(error => {
        console.error("Error forward ");
        winlogger.error(error.message);
        res.status(500).json({status: 'error' , error : error.message});
      })
  });

router.post('/register/complete', function(req, res, next) {
    winlogger.info("使用者完成FIDO Key 指紋辨識，正在重定向至FIDO Server 進行註冊完成..")
    const requestData = req.body 
   
    
    axios.post('http://de.yunpoc.edu.tw:5000/register/complete' , requestData)
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