import paramiko
import threading
import sys
import socket
import json
import log_config

logger = log_config.logger

# 定義一個 SSH 伺服器類別
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
        
    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL
    
    def check_channel_shell_request(self, channel):
        return True
            

def ssh_connect_and_interact(host, port, username, password, chan):
    # 創建 Transport 對象
    trans = paramiko.Transport((host, port))
    try:
        # 啟動 client
        trans.start_client()       
        # 認證憑證
        trans.auth_password(username=username, password=password)
        # 打開 session channel (for RP )
        channel = trans.open_session()
        channel.get_pty()
        channel.invoke_shell()
        
        def read_from_channel(channel):
            buffer = ""
            chk = False
            while True:
                if channel.recv_ready():
                    buffer = channel.recv(1024).decode('utf-8')
                    # 傳送給 agent，處理整行        
                    if '\n' in buffer and chk:
                        line, buffer = buffer.split('\n', 1)
                        chan.send(line)
                        chan.send(buffer)
                    else:
                        chan.send(buffer)
                        chk = True
                    
        # 開始一個 thread 來讀取 RP 端發送的輸出
        connect_rp = threading.Thread(target=read_from_channel, args=(channel,), daemon=True)
        
        connect_rp.start()

        while True:
            command = chan.recv(1024)
            if command == b'\x03' or command == b'':  # Ctrl+C
                print("中斷連線")
                channel.send("中斷連線")
                break
            print(command.decode('utf-8'))
            channel.send(command)
        connect_rp.join(timeout=1)
    finally:
        # 關閉通道及傳輸
        channel.close()
        trans.close()
        

# SSH 伺服器主要運行程式碼
def start_ssh_server():
    try:
        with open('chk.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
                        
        host = data['host']
        port = 22
        username = 'linuxrp'
        password = 'linuxrp'
        
        
        # 伺服器的 RSA 金鑰
        host_key = paramiko.RSAKey.from_private_key_file('/etc/ssh/ssh_host_rsa_key')
        
        ssh_server = SSHServer()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 2223))
        server_socket.listen(100)
        print("等待連接......")
        
        client_socket, client_addr = server_socket.accept()
        print(f"與 {client_addr} 建立連接")
        
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(host_key)
        transport.start_server(server=ssh_server)
        
        chan = transport.accept(20)
        if chan is None:
            print('*** No channel.')
            return False
        print('[+] 連接成功！')
        logger.info("USER %s ACCESS %s , PORT %s", client_addr, data['host'], "22")
        chan.send('\r\nWelcome to My SSH Server!\r\n')
        
        ssh_connect_and_interact(host, port, username, password, chan)
    except Exception as e:
        print(f"SSH 伺服器出現錯誤: {e}")
    finally:
        print("等待重新連線")
        return False


def run_servers():
    while True:
        # 建立線程
        ssh_thread = threading.Thread(target=start_ssh_server, daemon=True)
        ssh_thread.start()
        
        # 等待線程完成
        ssh_thread.join()
        
        print("線程已結束，重新啟動...")

# 開始運行伺服器
#run_servers()
