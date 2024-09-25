package view

import (
	"bytes"
	"encoding/json"
	"fmt"
	"html/template"
	"io"
	"net/http"

	"agweb/component"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"golang.org/x/crypto/ssh"
)

var (
	//Allow cross-domain
	upgrader = websocket.Upgrader{
		CheckOrigin: func(r *http.Request) bool {
			return true
		},
	}
	user     = "defaultUser"
	password = "linuxrp"
	host     = "192.168.50.223"
	port     = 22
)

type UsernameResponse struct {
	Username string `json:"username"`
}

func fetchUsername() (string, error) {
	url := "http://de.yuntech.poc.com/web/login/begin"
	reqBody := []byte(`{"key":"value"}`)
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(reqBody))
	if err != nil {
		return "", fmt.Errorf("failed to fetch username: %v", err)
	}
	defer resp.Body.Close()

	// 使用 io.ReadAll 代替 ioutil.ReadAll
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("failed to read response body: %v", err)
	}

	var usernameResp UsernameResponse
	if err := json.Unmarshal(body, &usernameResp); err != nil {
		return "", fmt.Errorf("failed to parse username response: %v", err)
	}

	return usernameResp.Username, nil
}

func wsHandle(c *gin.Context) {
	var (
		conn    *websocket.Conn
		client  *ssh.Client
		sshConn *component.SSHConnect
		err     error
	)

	user, err = fetchUsername()
	if err != nil {
		fmt.Println("Error fetching username:", err)
		// 可以考慮在這裡返回錯誤訊息給 WebSocket 客戶端
		return
	}

	// Upgrade Gin context to WebSocket connection
	conn, err = upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		return
	}
	defer conn.Close()

	// Create ssh client
	if client, err = component.CreateSSHClient(user, password, host, port); err != nil {
		component.WsSendText(conn, []byte(err.Error()))
		return
	}
	defer client.Close()

	// Connect to ssh
	if sshConn, err = component.NewSSHConnect(client); err != nil {
		component.WsSendText(conn, []byte(err.Error()))
		return
	}

	quit := make(chan int)
	go sshConn.Output(conn, quit)
	go sshConn.Recv(conn, quit)
	<-quit
}
func home(w http.ResponseWriter, r *http.Request) {
	temp, e := template.ParseFiles("./template/index.html")
	if e != nil {
		fmt.Println(e)
	}
	temp.Execute(w, nil)
	return
}

func SSHRoutes(c *gin.Engine) {

	proxyGrop := c.Group("/sshpage")

	proxyGrop.Static("/static/css", "./static/css")
	proxyGrop.Static("/static/js", "./static/js")
	proxyGrop.Static("/static/img", "./static/img")

	proxyGrop.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "sshindex.html", nil)
	})

	proxyGrop.GET("/ssh", func(c *gin.Context) {
		c.HTML(http.StatusOK, "ssh.html", nil)
	})

	proxyGrop.GET("/ws/v1", wsHandle)

}
