CREATE DATABASE IF NOT EXISTS PROXYDB;

use `PROXYDB`;

CREATE TABLE IF NOT EXISTS `proxy_hosts` (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Source VARCHAR(255),
    Destination VARCHAR(255),
    Port VARCHAR(10),
    Description VARCHAR(255),
    Created datetime
);
