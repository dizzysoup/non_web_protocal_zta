// db.js

import mysql from 'mysql2/promise'; // 使用 Promise-based 的 mysql2 模組

// 設定資料庫連接的配置
const dbConfig = {
  host: 'fido2_db',    // 資料庫主機
  user: 'user',         // 資料庫使用者名稱
  password: 'password', // 資料庫密碼
  database: 'fido2',    // 資料庫名稱
};

// 建立資料庫連接池
const pool = mysql.createPool(dbConfig);

// 測試資料庫連接
pool.getConnection()
  .then(connection => {
    console.log('Connected Success to MySQL database');
    connection.release(); // 釋放連接
  })
  .catch(error => {
    console.error('Error connecting to MySQL:', error.message);
  });

export default pool;
