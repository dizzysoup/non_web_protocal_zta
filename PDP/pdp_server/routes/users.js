import express from 'express';
import axios from 'axios';
import pool from '../components/db.js'; 


var router = express.Router();


/* GET users listing. */
router.get('/', async function(req, res, next) {
    try {
      const query = `
        SELECT u.id , u.username , u.email , u.created_at , c.aaguid, c.credential_id , c.public_key 
        FROM users u 
        JOIN credentialData c ON u.username = c.username       
        `;
        const [rows] = await pool.query(query);
        res.status(200).json(rows);
      } catch (err) {
        console.error(err);
        res.status(500).send("伺服器錯誤");
      }
});

router.get('/credentials', async function(req, res, next) {
    try {
        const [rows] = await pool.query('SELECT * FROM credentialData');
        res.status(200).json(rows);
      } catch (err) {
        console.error(err);
        res.status(500).send("伺服器錯誤");
      }
});

router.delete('/credentials/:username', async (req, res) => {
    const { aaguid } = req.params;
    try {
      const [result] = await pool.query('DELETE FROM credentialData WHERE username = ?', [aaguid]);
      if (result.affectedRows === 0) {
        return res.status(404).send("找不到該憑證");
      }
      res.status(200).send("憑證刪除");
    } catch (err) {
      console.error(err);
      res.status(500).send("伺服器錯誤");
    }
  });
//測試
router.use(express.json());  // 允許 Express 解析 JSON 請求體

// 刪除特定使用者
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    try {
      const [result] = await pool.query('DELETE FROM users WHERE id = ?', [id]);
      if (result.affectedRows === 0) {
        return res.status(404).send("找不到該使用者");
      }
      res.status(200).send("使用者已刪除");
    } catch (err) {
      console.error(err);
      res.status(500).send("伺服器錯誤");
    }
  });


export default router ; 