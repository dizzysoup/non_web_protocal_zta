import express from "express";
import pool from "../components/db.js";
var router = express.Router();

/* GET home page. */
router.get('/', async function(req, res, next) {
  try {
    const [rows] = await pool.query('SELECT 1 ');
    console.log(rows);
  }catch (error){
    console.error('Error fetching data:', error.message);
  }
  res.redirect('https://de.yuntech.poc.com:5443')
});

router.post('/', function(req, res, next) {
  var username = req.body.username;
  var password = req.body.password;

  res.json({ status: 'success', message: 'Received username and password successfully.' });
});

export default router
