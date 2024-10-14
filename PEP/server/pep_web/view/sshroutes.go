package view

import (
	"agweb/component"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"golang.org/x/crypto/ssh"
)

type ConnectingRP struct {
	IPAddress string `json:"ip_address" binding:"required"`
	Port      int    `json:"port" binding:"required"`
	Username  string `json:"username" binding:"required"`
}

func wsHandle(c *gin.Context) {
	var (
		conn    *websocket.Conn
		client  *ssh.Client
		sshConn *component.SSHConnect
		err     error
	)

	var (
		//Allow cross-domain
		upgrader = websocket.Upgrader{
			CheckOrigin: func(r *http.Request) bool {
				return true
			},
		}
		user           = savedRP.Username
		host           = savedRP.IPAddress
		port           = 22              // 目標主機端口
		privateKeyPath = "./cert/id_rsa" // 私鑰文件的路徑
	)

	// 升級 Gin context 為 WebSocket 連接
	conn, err = upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		return
	}
	defer conn.Close()

	// 使用私鑰創建 SSH 客戶端
	client, err = component.CreateSSHClientWithKey(user, host, port, privateKeyPath)
	if err != nil {
		component.WsSendText(conn, []byte(err.Error()))
		return
	}
	defer client.Close()

	// 創建 SSH 連接
	sshConn, err = component.NewSSHConnect(client)
	if err != nil {
		component.WsSendText(conn, []byte(err.Error()))
		return
	}

	// 啟動 SSH 輸出和接收處理
	quit := make(chan int)
	go sshConn.Output(conn, quit)
	go sshConn.Recv(conn, quit)
	<-quit
}

var savedRP ConnectingRP

func SSHRoutes(c *gin.Engine) {

	proxyGroup := c.Group("/RemotePage")

	proxyGroup.Static("/static/css", "./static/css")
	proxyGroup.Static("/static/js", "./static/js")
	proxyGroup.Static("/static/img", "./static/img")

	proxyGroup.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "sshindex.html", nil)
	})

	proxyGroup.POST("/", func(c *gin.Context) {
		var req ConnectingRP

		// 綁定 JSON 資料到 ConnectRequest 結構體
		if err := c.ShouldBindJSON(&req); err != nil {
			// 如果出現錯誤，回傳錯誤訊息
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		savedRP = req
		// 回傳成功訊息
		c.JSON(http.StatusOK, gin.H{
			"message": "Connection successful",
		})
	})

	proxyGroup.GET("/ssh", func(c *gin.Context) {
		c.HTML(http.StatusOK, "ssh.html", nil)
	})

	proxyGroup.GET("/ssh/windows", func(c *gin.Context) {
		c.HTML(http.StatusOK, "rdpindex.html", nil)
	})

	// 新增處理 RDP WebSocket 請求的路由
	proxyGroup.GET("/ws/rdp", RdpProxy)

	proxyGroup.GET("/ws/v1", wsHandle)
}
