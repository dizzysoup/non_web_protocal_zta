import express from 'express';
import {Client} from 'ssh2' ;
import winlogger from '../components/log.js';
import fs from 'fs';
import process from 'process';

// 新增遠端使用者
function CreateUserFromLinuxRP(username, ip_address) {
    return new Promise((resolve, reject) => {        
        const sshConfig = {
            host: ip_address, // 遠端Linux的IP位址
            port: 22, // SSH端口，預設為22
            username: "root", // SSH使用者名稱      
            password: "linuxrp"                  
        };
        
        const publicKey = fs.readFileSync('cert/id_rsa.pub');
        const conn = new Client();
        conn.on('ready', () => {
            // 構建新增使用者的命令
            const addUserCommand = `sudo useradd -m ${username} &&  sudo mkdir -p /home/${username}/.ssh &&  sudo chmod 700 /home/${username}/.ssh &&
                echo "${publicKey}" | sudo tee /home/${username}/.ssh/authorized_keys &&
                sudo chmod 600 /home/${username}/.ssh/authorized_keys &&
                sudo chown -R ${username}:${username} /home/${username}/.ssh
            `;

            winlogger.info(addUserCommand);

            conn.exec(addUserCommand, (err, stream) => {
                if (err) {
                    winlogger.info('SSH 指令執行失敗', err);
                    conn.end(); // 關閉連線
                    return reject(new Error('新增使用者失敗'));
                }

                stream.on('close', (code, signal) => {
                    winlogger.info('SSH 指令執行結束');
                    conn.end();
                    if (code === 0) {
                        resolve(true); // 操作成功
                    } else {
                        reject(new Error('遠端新增使用者失敗， 可能已經存在該使用者或是其他錯誤，請再加確認'));
                    }
                }).on('data', (data) => {
                    winlogger.info('STDOUT: ' + data);
                }).stderr.on('data', (data) => {
                    winlogger.info('STDERR: ' + data);
                });
            });
        }).on('error', (err) => {
            winlogger.info('SSH 連接錯誤', err);
            reject(new Error('SSH 連接失敗'));
        }).connect(sshConfig);
    });
}

// 刪除遠端使用者
function DeleteRemoteUserFromLinuxRP(username, ipAddress) {
    return new Promise((resolve, reject) => {
        const sshConfig = {
            host: ipAddress,
            port: 22,
            username: 'root', // 使用 root 或具備適當權限的使用者
            password: 'linuxrp' // SSH 使用者的密碼
        };
        const conn = new Client();
        conn.on('ready', () => {
            // 構建新增使用者的命令
            const deleteUserCommand = `sudo userdel -r ${username}`;

            conn.exec(deleteUserCommand, (err, stream) => {
                if (err) {
                    winlogger.info('SSH 指令執行失敗', err);
                    conn.end(); // 關閉連線
                    return reject(new Error('新增使用者失敗'));
                }

                stream.on('close', (code, signal) => {
                    winlogger.info('SSH 指令執行結束');
                    conn.end();
                    if (code === 0) {
                        resolve(true); // 操作成功
                    } else {
                        reject(new Error('遠端新增使用者失敗， 可能已經存在該使用者或是其他錯誤，請再加確認'));
                    }
                }).on('data', (data) => {
                    winlogger.info('STDOUT: ' + data);
                }).stderr.on('data', (data) => {
                    winlogger.info('STDERR: ' + data);
                });
            });
        }).on('error', (err) => {
            winlogger.info('SSH 連接錯誤', err);
            reject(new Error('SSH 連接失敗'));
        }).connect(sshConfig);
        
    });
}

export{
    CreateUserFromLinuxRP , 
    DeleteRemoteUserFromLinuxRP
}