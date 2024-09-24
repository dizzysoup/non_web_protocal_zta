import express from 'express';
import axios from 'axios';
var router = express.Router();


/* GET users listing. */
router.get('/', function(req, res, next) {
  res.send('respond with a resource???');
});

//測試
router.use(express.json());  // 允許 Express 解析 JSON 請求體

// 定義 POST 路由來接收 /username 請求並轉發給 FIDO2
router.post('/', async (req, res) => {
    const { username } = req.body;
    if (username) {
      try {
          // 發送請求至 FIDO2 伺服器
          const fidoResponse = await axios.post('http://192.168.50.76:5000/fido2test', { username });
          const fidoData = fidoResponse.data;
  
          // 將數據返回至 PEP
          res.status(200).json({
              message: `PDP 處理完成，FIDO2 伺服器回應: ${fidoData.message || "未提供訊息"}`,
              data: fidoData
          });
      } catch (error) {
          console.error(`轉發至 FIDO2 伺服器時發生錯誤: ${error.message}`);
          res.status(500).send('轉發至 FIDO2 伺服器時發生錯誤');
      }
  } else {
      res.status(400).send('需要提供使用者名稱');
  }
  });

export default router ; 