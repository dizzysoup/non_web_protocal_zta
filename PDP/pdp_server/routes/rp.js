import express from "express";
import pool from '../components/db.js';


var router = express.Router();

// 取得所有電腦資料
router.get('/', async (req, res) => {
    try {
      const [rows] = await pool.query('SELECT * FROM RP_Computers');
      res.json(rows);
    } catch (error) {
      console.error('Error fetching data:', error.message);
      res.status(500).json({ error: 'Error fetching data' });
    }
  });

// 取得特定電腦資料
router.get('/:id', async (req, res) => {
    const { id } = req.params;
    try {
      const [rows] = await pool.query('SELECT * FROM RP_Computers WHERE id = ?', [id]);
      if (rows.length === 0) {
        return res.status(404).json({ error: 'Computer not found' });
      }
      res.json(rows[0]);
    } catch (error) {
      console.error('Error fetching data:', error.message);
      res.status(500).json({ error: 'Error fetching data' });
    }
  });


// 新增電腦資料
router.post('/', async (req, res) => {
    const { alias_name, ip_address, domain_name, port, os_type, description } = req.body;
    try {
      const [result] = await pool.query(
        'INSERT INTO RP_Computers (alias_name, ip_address, domain_name, port, os_type, description) VALUES (?, ?, ?, ?, ?, ?)',
        [alias_name, ip_address, domain_name, port, os_type, description]
      );
      res.status(201).json({ message: 'Computer added', id: result.insertId });
    } catch (error) {
      console.error('Error adding computer:', error.message);
      res.status(500).json({ error: 'Error adding computer' });
    }
  });

// 更新電腦資料
router.put('/:id', async (req, res) => {
    const { id } = req.params;
    const { alias_name, ip_address, domain_name, port, os_type, description } = req.body;
    try {
      const [result] = await pool.query(
        'UPDATE RP_Computers SET alias_name = ?, ip_address = ?, domain_name = ?, port = ?, os_type = ?, description = ? WHERE id = ?',
        [alias_name, ip_address, domain_name, port, os_type, description, id]
      );
      if (result.affectedRows === 0) {
        return res.status(404).json({ error: 'Computer not found' });
      }
      res.json({ message: 'Computer updated' });
    } catch (error) {
      console.error('Error updating computer:', error.message);
      res.status(500).json({ error: 'Error updating computer' });
    }
  });

// 刪除電腦資料
router.delete('/:id', async (req, res) => {
    const { id } = req.params;
    try {
      const [result] = await pool.query('DELETE FROM RP_Computers WHERE id = ?', [id]);
      if (result.affectedRows === 0) {
        return res.status(404).json({ error: 'Computer not found' });
      }
      res.json({ message: 'Computer deleted' });
    } catch (error) {
      console.error('Error deleting computer:', error.message);
      res.status(500).json({ error: 'Error deleting computer' });
    }
  });
  

export default router