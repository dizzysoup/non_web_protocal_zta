-- 初始化資料庫和表格

-- 使用或創建資料庫
CREATE DATABASE IF NOT EXISTS fido2;

CREATE USER 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON fido2.* TO 'user'@'%';

-- 使用資料庫
USE fido2;

-- 創建使用者表
CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY, -- user 識別唯一值
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (username)
) ;

-- 創建 credentialData 表
CREATE TABLE IF NOT EXISTS credentialData (
  aaguid CHAR(36),
  credential_id VARCHAR(255) NOT NULL,
  public_key JSON NOT NULL,
  username VARCHAR(50),
  PRIMARY KEY (aaguid , username ),
  CONSTRAINT fk_username FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE
) ;

-- RP 表
CREATE TABLE IF NOT EXISTS RP_Computers (
  id INT AUTO_INCREMENT PRIMARY KEY, -- 唯一識別每台電腦的ID
  alias_name VARCHAR(255) NOT NULL , -- 電腦的別名
  ip_address VARCHAR(45) NOT NULL ,  -- IP 地址
  domain_name VARCHAR(255) NULL, -- 電腦的域名
  port ENUM('3389','22') NOT NULL , -- 連接埠號 (如 3389, 22 等)
  os_type ENUM('Linux' , 'Windows') NOT NULL , -- 作業系統類型
  description TEXT NULL , -- 敘述
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- RP 對應 User 表
CREATE TABLE IF NOT EXISTS User_Maintained_Computers (
  user_id INT,  -- 使用者 ID，來自 users 表
  computer_id INT,  -- 電腦 ID，來自 RP_Computers 表
  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 指派日期
  PRIMARY KEY (user_id, computer_id),  -- 確保每位使用者對應到每台電腦只有一個關係
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,  -- 設定外鍵並在使用者刪除時一併刪除關係
  FOREIGN KEY (computer_id) REFERENCES RP_Computers(id) ON DELETE CASCADE  -- 設定外鍵並在電腦刪除時一併刪除關係
);


FLUSH PRIVILEGES;