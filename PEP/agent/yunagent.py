from fido2.hid import CtapHidDevice
from fido2.client import Fido2Client, WindowsClient, UserInteraction
from fido2.server import Fido2Server
from fido2.cose import ES256 
from gRPC.gRPC import CredentialClient , RPManagerClient
from rdp_client import start_rdp
from getpass import getpass
import sys
import ctypes
import subprocess
import argparse
import paramiko
import time 
import socket
import select 
import sys 
import json 
import os

try:
    from fido2.pcsc import CtapPcscDevice
except ImportError:
    CtapPcscDevice = None


uv = "discouraged"

# 憑證儲存
def store_credential_files(user_id, credential):
    # 提取 credential 的各個屬性並轉換為可序列化的格式
    credential_id = credential["credential_id"].hex()
    public_key = {
        k: v.hex() if isinstance(v, bytes) else v
        for k, v in credential["public_key"].items()
    }
    sign_count = 0  # 假設初始簽名計數為 0
    transports = "usb"  # 假設默認傳輸方式為 USB
    aaguid = credential["aaguid"].hex()
   
    # 將屬性轉換為字典格式
    credential_data = {
        "user_id": user_id.decode("utf-8"),
        "public_key": public_key,
        "sign_count": sign_count,
        "transports": transports,
        "aaguid": aaguid,
        "credential_id": credential_id,
    }
    
    # 將字典格式轉換為 JSON 並儲存到文件中
    filename = f'credentials/credential.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(credential_data, f, indent=4)
    return credential_data

# 憑證提取 by dict 
def load_credential_files_by_dict():
    # 從文件中加載 JSON 數據
    with open('credentials/credential.json', 'r') as f:
        credential_data = json.load(f)   
    # 如果 credential_data 是一個字典，將其包裝成一個列表
    if isinstance(credential_data, dict):
        credential_data = [credential_data]
    # 組裝為 AttestedCredentialData 的列表
    credentials = [AttestedCredentialData.from_dict(data) for data in credential_data]
    # 組裝為原始格式的字典
    return credentials

# 憑證提取 by json 
def load_credential_files_by_json():
    # 從文件中加載 JSON 數據
    with open('credentials/credential.json', 'r') as f:
        credential_data = json.load(f)   
    return credential_data

# 更新data 、暫存可以刪
def update_json_file(file_path, updates):
    # 读取现有的 JSON 文件内容
    with open(file_path, 'r') as f:
        data = json.load(f)

    # 更新指定的键值
    for key, value in updates.items():
        if key in data:
            data[key] = value

    # 将更新后的内容写回 JSON 文件
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def enumerate_devices():
    for dev in CtapHidDevice.list_devices():
        yield dev
    if CtapPcscDevice:
        for dev in CtapPcscDevice.list_devices():
            yield dev


index = 0 

class AttestedCredentialData:
    def __init__(self, aaguid, credential_id, public_key):        
        self.aaguid = aaguid
        self.credential_id =credential_id
        self.public_key =  ES256(public_key)
        
    @staticmethod
    def from_dict(data):
        print(data['aaguid'])
        aaguid = bytes.fromhex(data['aaguid'])
        credential_id = bytes.fromhex(data['credential_id'])
        public_key = {
            int(k): bytes.fromhex(v) if isinstance(v, str) and all(c in '0123456789abcdef' for c in v) else v
            for k, v in data['public_key'].items()
        }
        return AttestedCredentialData(aaguid, credential_id, public_key
)
# Handle user interaction
class CliInteraction(UserInteraction):
    def prompt_up(self):
        print("\nTouch your authenticator device now...\n")

    def request_pin(self, permissions, rd_id):
        return getpass("Enter PIN: ")

    def request_uv(self, permissions, rd_id):
        print("User Verification required.")
        return True


if WindowsClient.is_available() and not ctypes.windll.shell32.IsUserAnAdmin():
    # Use the Windows WebAuthn API if available, and we're not running as admin
    client = WindowsClient("https://example.com")
else:
    # Locate a device
    for dev in enumerate_devices():
        client = Fido2Client(
            dev, "https://example.com", user_interaction=CliInteraction()
        )
        if client.info.options.get("rk"):
            break
    else:
        print("No Authenticator with support for resident key found!")
        sys.exit(1)

    # Prefer UV if supported
    if client.info.options.get("uv"):
        uv = "preferred"
        print("Authenticator supports User Verification")

parser = argparse.ArgumentParser(description='Example script with a positional argument.')
subparsers = parser.add_subparsers(dest='command', help='sub-command help')

# register sub-command
register_parser = subparsers.add_parser('register', help='register help')
register_parser.add_argument('--pep' , type=str , help='The PEP address')
register_parser.add_argument('--user', type=str, help='The username')

#login sub-command
login_parser = subparsers.add_parser('login', help='login help')
login_parser.add_argument('--pep' , type=str , help='The PEP address')
login_parser.add_argument('--user', type=str, help='The username')

# logout sub-command
logout_parser = subparsers.add_parser('logout', help='logout help')

# ssh sub-command
ssh_parser = subparsers.add_parser('ssh', help='ssh command')
ssh_parser.add_argument("argtext", type=str, help="SSH command <username>@<IP or Domain >")

# rdp sub-command
rdp_parser = subparsers.add_parser('rdp', help='rdp command')
rdp_parser.add_argument("--rp", type=str, help="RP command")
rdp_parser.add_argument("--user", type=str, help="User command")



# parser.add_argument('argtext', help='IP address to connect')

args = parser.parse_args()
print(args)
server = Fido2Server({"id": "example.com", "name": "Example RP"}, attestation="direct")
credentials_data = "" 
match args.command:
    case "register" :
        pep_address = args.pep
        username = args.user
        user = {"id": str(index).encode("utf-8") , "name": username}
        # Prepare parameters for makeCredential
        create_options, state = server.register_begin(
            user,
            resident_key_requirement="required",
            user_verification=uv,
            authenticator_attachment="cross-platform",
        )       
        # Create a credential
        result = client.make_credential(create_options["publicKey"])
        # Complete registration
        auth_data = server.register_complete(
            state, result.client_data, result.attestation_object
        )
        
        credential_data = [auth_data.credential_data]
        print(credential_data)
        credentials = {
            "aaguid": credential_data[0].aaguid,
            "credential_id": credential_data[0].credential_id,
            "public_key": credential_data[0].public_key
        }
        
        print("New credential created!")
        # 於本地端儲存憑證
        credentials = store_credential_files(user["id"], credentials)   
        pep_address += ':50051'
        

        # 傳送憑證到server -- '192.168.71.3:50051'        
        client_cre = CredentialClient(pep_address)
        client_cre.send_credentials_to_server(user["id"], credentials)
        
        
        ##  ============================= 以下是追加的，credential_data 目前無解 ### ============================================
        print(credential_data)
        request_options, state = server.authenticate_begin(credential_data,user_verification=uv)
        
        # Authenticate the credential
        selection = client.get_assertion(request_options["publicKey"])
        result = selection.get_response(0)  # There may be multiple responses, get the first.
        

        # 傳送憑證到server -- '192.168.71.3:50051'       
       
        rpcclient = CredentialClient(pep_address)
        rpcclient.send_credentials_to_auth(0, load_credential_files_by_json())
        
        # server 端驗證
        server.authenticate_complete(
            state,
            [credential_data],
            result.credential_id,
            result.client_data,
            result.authenticator_data,
            result.signature,
        )
        print("Credential authenticated!")
        
        update_json_file('credentials/data.json', {'pep_auth': True, 'pep_ip':  args.pep})
        
    case "login" : 
        pep_address = args.pep
        username = args.user

        # 讀取憑證
        credential = load_credential_files_by_dict()  
            
        print(credential)
        
        # Prepare parameters for getAssertion
        request_options, state = server.authenticate_begin(credential,user_verification=uv)
        
        # Authenticate the credential
        selection = client.get_assertion(request_options["publicKey"])
        result = selection.get_response(0)  # There may be multiple responses, get the first.
        

        # 傳送憑證到server -- '192.168.71.3:50051'       
        pep_address += ':50051' 
        rpcclient = CredentialClient(pep_address)
        rpcclient.send_credentials_to_auth(0, load_credential_files_by_json())
        
        # server 端驗證
        server.authenticate_complete(
            state,
            [credential],
            result.credential_id,
            result.client_data,
            result.authenticator_data,
            result.signature,
        )
        print("Credential authenticated!")
        
        update_json_file('credentials/data.json', {'pep_auth': True, 'pep_ip':  args.pep})
        
    case "ssh":      
        with open('credentials/data.json', 'r') as f:
           data = json.load(f) 
        if data.get("pep_auth") == False:
            print("Please login first")
            sys.exit(1)
        
        ip = args.argtext.split('@')[1]
        user = args.argtext.split('@')[0]
        # 檢查該RP 是否有註冊
        pep_address = data.get("pep_ip") + ":50051"        
        rpcclient = RPManagerClient(pep_address)
        response = rpcclient.check_rp_registration(ip)
        if(response.is_registered == False):
            print("The IP address or Domain is not registered")
            sys.exit(1)
        
        arg = "yunpep@" + data.get("pep_ip")
        
        user = {"id": str(index).encode("utf-8") , "name": args.argtext.split('@')[0]}     
        command = ["ssh" ,  arg , "-p" , "2223"]   
        subprocess.run(command, check=True)
    case "rdp" :
        rp_ip = args.rp
        username = args.user
        # 檢查該RP 是否有註冊
        with open('credentials/data.json', 'r') as f:
           data = json.load(f) 
        pep_address = data.get("pep_ip") + ":50051" 
        rpcclient = RPManagerClient(pep_address)
        response = rpcclient.check_rp_registration(rp_ip)
        if(response.is_registered == False):
            print("The IP address or Domain is not registered")
            sys.exit(1)
        
        start_rdp(data.get("pep_ip"), username)
    case "logout" : 
       update_json_file('credentials/data.json', {'pep_auth': False, 'pep_ip': ''})
       print("Logout successfully")

        
        
        
