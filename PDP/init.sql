-- 初始化資料庫和表格

-- 使用或創建資料庫
CREATE DATABASE IF NOT EXISTS fido2;

CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON fido2.* TO 'user'@'%';

-- 使用資料庫
USE fido2;

-- 創建使用者表
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (username)
) ;

-- 創建 credentialData 表
CREATE TABLE IF NOT EXISTS credentialData (
  aaguid CHAR(36),
  credential_id BLOB NOT NULL,
  public_key JSON NOT NULL,
  username VARCHAR(50),
  PRIMARY KEY (aaguid , username ),
  CONSTRAINT fk_username FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE
) ;



FLUSH PRIVILEGES;