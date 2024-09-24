package main

import (
	"agweb/view" // 替換為實際專案路徑
	"fmt"
	"log"

	"github.com/gin-gonic/gin"
)

func main() {

	fmt.Println("Successfully connected to the database!")

	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.Static("/static", "./static")

	// 註冊路由
	view.ProxyRegisterRoutes(r)
	view.WebauthRegisterRoutes(r)
	view.SSHRoutes(r)

	certFile := "./cert/server.crt"
	keyFile := "./cert/private.key"
	err := r.RunTLS(":8080", certFile, keyFile)
	if err != nil {
		log.Fatal("Failed to start HTTPS server : ", err)
	}

}
