import subprocess
import time
import pyautogui

# 啟動RDP客戶端
def start_rdp(ip, username):
    # 建立RDP文件內容
    rdp_content = f"""
screen mode id:i:2
use multimon:i:0
desktopwidth:i:1280
desktopheight:i:800
session bpp:i:32
winposstr:s:0,3,0,0,800,600
compression:i:1
keyboardhook:i:2
audiocapturemode:i:0
videoplaybackmode:i:1
connection type:i:2
networkautodetect:i:1
bandwidthautodetect:i:1
displayconnectionbar:i:1
username:s:{username}
enableworkspacereconnect:i:0
disable wallpaper:i:0
allow font smoothing:i:0
allow desktop composition:i:0
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
full address:s:{ip}
audiomode:i:0
redirectprinters:i:1
redirectcomports:i:0
redirectsmartcards:i:1
redirectclipboard:i:1
redirectposdevices:i:0
autoreconnection enabled:i:1
authentication level:i:2
prompt for credentials:i:0
negotiate security layer:i:1
remoteapplicationmode:i:0
alternate shell:s:
shell working directory:s:
gatewayhostname:s:
gatewayusagemethod:i:4
gatewaycredentialssource:i:4
gatewayprofileusagemethod:i:0
promptcredentialonce:i:1
use redirection server name:i:0
rdgiskdcproxy:i:0
kdcproxyname:s:
"""

    # 將RDP內容寫入文件
    with open('temp.rdp', 'w') as file:
        file.write(rdp_content)

    # 使用mstsc命令打開RDP文件
    subprocess.run(['mstsc', 'temp.rdp'])

    # 給RDP界面一些時間來啟動
    time.sleep(5)


