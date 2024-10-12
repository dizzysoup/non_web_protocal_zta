import express from "express";
import pool from '../components/db.js';
import {CreateUserFromLinuxRP , DeleteRemoteUserFromLinuxRP }from "../components/linuxuser.js";
import winlogger from '../components/log.js';


var router = express.Router();

// 列出所有 User_Maintained_Computers 資料
router.get('/', async (req, res) => {
    try {
      const query = `
        SELECT umc.user_id,u.username,umc.computer_id, rp.alias_name, rp.ip_address, rp.domain_name, rp.port, rp.os_type, rp.description, rp.created_at
        FROM User_Maintained_Computers umc
        JOIN users u ON umc.user_id = u.id
        JOIN RP_Computers rp ON umc.computer_id = rp.id
    `;

      const [rows] = await pool.query(query);
      res.status(200).json(rows);
    } catch (err) {
      console.error(err);
      res.status(500).send("伺服器錯誤");
    }
  });


// 針對單一 user_id 撈出資料  (加上status true /false 都會觸發)
router.get('/:user_id', async (req, res) => {
  const { user_id } = req.params;
  try {
    const query = `
      SELECT 
          IF(umc.user_id IS NOT NULL, 'true', 'false') AS status,
          rp.id,
          rp.alias_name,
          rp.ip_address,
          rp.port,
          rp.os_type
      FROM 
          RP_Computers rp
      LEFT JOIN 
          User_Maintained_Computers umc 
      ON 
          rp.id = umc.computer_id 
      AND 
          umc.user_id = ?; 
    `;
    const [rows] = await pool.query(query, [user_id]);

    res.status(200).json(rows);
  } catch (err) {
    console.error(err);
    return res.status(500).send("伺服器錯誤");
  }
});
// 針對單一 user_id 撈出資料 
router.get('/allow/:user_id' , async (req , res ) => {
  const { user_id } = req.params;
  try {
    const query = `
      SELECT           
          rp.id,
          rp.alias_name,
          rp.ip_address,
          rp.port,
          rp.os_type
      FROM 
          RP_Computers rp
      JOIN 
          User_Maintained_Computers umc 
      ON 
          rp.id = umc.computer_id 
      AND 
          umc.user_id = ?; 
    `

    const [rows] = await pool.query(query, [user_id]);
    if (rows.length === 0) {
      return res.status(404).send("該使用者沒有維護的電腦資料");
    }

    res.status(200).json(rows);
  }catch (err) {
    console.error(err);
    return res.status(500).send("伺服器錯誤" + err.message());
  }
})


// 刪除某個使用者與電腦的關係
router.delete('/:user_id/:computer_id', async (req, res) => {
  try {
      const { user_id, computer_id } = req.params;
      
      const selectQuery = `
          SELECT u.username, r.ip_address, r.port, r.os_type
          FROM users u
          JOIN RP_Computers r
          JOIN User_Maintained_Computers umc ON umc.user_id = u.id AND umc.computer_id = r.id
          WHERE u.id = ? AND r.id = ?;
      `;

      // 使用 await 來處理 pool.query
      const [rows] = await pool.query(selectQuery, [user_id, computer_id]);

      // 檢查是否有結果
      if (rows.length === 0) {
          return res.status(404).send("使用者與電腦的關係不存在");
      }

      const { username, ip_address, port, os_type } = rows[0];
      winlogger.info(`準備刪除使用者 ${username}`);

      // 檢查是否符合條件進行刪除
      if (port == 22 && os_type === 'Linux') {
          try {
              const deleteResult = await DeleteRemoteUserFromLinuxRP(username, ip_address);
              winlogger.info(deleteResult);
              
              // 刪除資料庫記錄
              const deleteQuery = 'DELETE FROM User_Maintained_Computers WHERE user_id = ? AND computer_id = ?';
              await pool.query(deleteQuery, [user_id, computer_id]);

              return res.status(200).send("使用者及遠端電腦刪除成功");
          } catch (err) {
              winlogger.error(`刪除遠端使用者失敗: ${err}`);
              return res.status(500).send(`刪除遠端使用者失敗: ${err.message}`);
          }
      } else {
          return res.status(400).send("不符合條件，無法刪除遠端使用者");
      }
  } catch (err) {
      winlogger.error(`伺服器錯誤: ${err}`);
      return res.status(500).send("伺服器錯誤");
  }
});



// 新增多筆 User_Maintained_Computers 資料
router.post('/', async (req, res) => {
    const entries = req.body; // 假設前端傳送過來的是一個陣列
    const user_id = entries[0]["user_id"];
    const computer_id = entries[0]["computer_id"];
    winlogger.info(`https://de.yuntech.poc.com:3443/maintained-computers POST ${user_id} : ${computer_id}`);

    if (!Array.isArray(entries) || entries.length === 0) {
      return res.status(400).send("請傳送一個包含資料的陣列");
    }

    const selectQuery = `
        SELECT u.username, r.ip_address, r.port , r.os_type
        FROM users u
        JOIN RP_Computers r ON r.id = ?
        WHERE u.id = ?
    `;

    const [rows] = await pool.query(selectQuery, [computer_id, user_id]);
    if(rows.affectedRows === 0 ){
      return res.status(404).send("使用者與電腦的關係不存在");
    }
    const { username , ip_address , port , os_type } = rows[0];
    
    winlogger.info(`使用者 ${username} 允許向 (${ip_address}, ${os_type} , ${port} )電腦新增使用者`)

    if(port == 22 && os_type == 'Linux'){
      // 新增遠端使用者
      CreateUserFromLinuxRP(username , ip_address).then(
        result => {
          winlogger.info("使用者新增成功",result);

          const query = "INSERT INTO User_Maintained_Computers (user_id, computer_id) VALUES (?, ?)";
          winlogger.info("將資料導入置資料庫中");

          pool.query(query, [user_id, computer_id])
          .then ( result => {
            winlogger.info(`User_Maintained_Computer 資料新增成功`);
            return res.status(200).send("新增成功");
          })           
          .catch(err => {
            winlogger.info("資料庫新增失敗", err);
            return res.status(500).send("" + err);
          });
      }).catch(err => {
        winlogger.info('伺服器內部錯誤 , ' , err);
        return res.status(500).send("" + err);
      });    
    }
    
  });


export default router