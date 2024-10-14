package component

import (
	"bytes"
	"fmt"
	"io/ioutil"

	"golang.org/x/crypto/ssh"
)

// 創建 SSH 客戶端，使用私鑰進行身份驗證
func CreateSSHClientWithKey(user, host string, port int, privateKeyPath string) (*ssh.Client, error) {
	// 讀取私鑰
	key, err := ioutil.ReadFile(privateKeyPath)
	if err != nil {
		return nil, fmt.Errorf("無法讀取私鑰文件: %v", err)
	}

	// 解析私鑰
	signer, err := ssh.ParsePrivateKey(key)
	if err != nil {
		return nil, fmt.Errorf("無法解析私鑰: %v", err)
	}

	// 設置 SSH 客戶端配置，使用私鑰進行身份驗證
	clientConfig := &ssh.ClientConfig{
		User: user,
		Auth: []ssh.AuthMethod{
			ssh.PublicKeys(signer),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(), // 略過主機密鑰檢查
	}

	// 拼接主機地址和端口
	addr := fmt.Sprintf("%s:%d", host, port)

	// 嘗試通過 SSH 連接到指定地址
	client, err := ssh.Dial("tcp", addr, clientConfig)
	if err != nil {
		return nil, fmt.Errorf("無法建立 SSH 連線: %v", err)
	}

	return client, nil
}

func runSSH(client *ssh.Client, command string) (string, error) {
	var err error
	var session *ssh.Session
	if session, err = client.NewSession(); err == nil {
		session.StdinPipe()
		defer session.Close()
		var stdOut bytes.Buffer

		session.Stdout = &stdOut
		err = session.Run(command)
		if err != nil {
			return "", err
		}

		return string(stdOut.Bytes()), nil
	}
	return "", err

}
