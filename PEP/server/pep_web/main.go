package main

import (
	"agweb/view" // 替換為實際專案路徑
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt"
)

func logPEPEvent(action string, user string, ip string, status string) {

	// 開啟或創建 PEP Log 檔案
	file, err := os.OpenFile("log.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatalf("無法打開 PEP log 檔案: %v", err)
	}
	defer file.Close()

	// 設定 Log 格式
	logMsg := fmt.Sprintf("[PEP LOG] - User: %s - Action: %s - Status: %s - IP: %s", user, action, status, ip)
	log.SetFlags(0)
	log.SetOutput(file)
	log.Println(logMsg)
}
func getTokenFromHeader(c *gin.Context) (string, error) {
	// 獲取 Authorization 標頭
	authHeader := c.GetHeader("Authorization")

	// 如果沒有 Authorization header，返回錯誤
	if authHeader == "" {
		return "", fmt.Errorf("Authorization header is missing")
	}

	// 檢查是否以 'Bearer ' 開頭
	if !strings.HasPrefix(authHeader, "Bearer ") {
		return "", fmt.Errorf("Authorization header format is invalid")
	}

	// 提取 Bearer 後的 token 部分
	token := strings.TrimPrefix(authHeader, "Bearer ")

	// 檢查 token 是否存在
	if token == "" {
		return "", fmt.Errorf("Token is missing")
	}

	return token, nil
}

func getUserFromJWT(c *gin.Context) string {
	// 檢查並獲取 token
	tokenString, err := getTokenFromHeader(c)
	if err != nil {
		fmt.Println("Authorization Error:", err)
		return "anonymous" // 如果 token 不存在或無效，返回匿名
	}

	// 解析 JWT token
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		// 使用你自己的密鑰來驗證 token
		return []byte("your_secret_key"), nil
	})

	if err != nil {
		fmt.Println("JWT Parse Error:", err)
		return "anonymous"
	}

	// 提取 JWT Claims 中的使用者資訊
	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		if user, exists := claims["username"].(string); exists {
			return user
		}
	}

	return "anonymous"
}
func main() {

	fmt.Println("Successfully connected to the database!")

	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.Static("/static", "./static")

	r.Use(func(c *gin.Context) {

		// 這裡可以擷取用戶 IP 和其他資訊
		ip := c.ClientIP()
		// 如果有用戶資訊或登入狀態，也可以在這裡獲取
		user := getUserFromJWT(c) //
		action := c.FullPath()    // 取得完整的 API 路徑作為操作
		status := "Accessing"     // 設定狀態，這裡是簡單的示例
		logPEPEvent(action, user, ip, status)
		c.Next()
	})

	// 註冊路由
	r.GET("/api/rdp", func(c *gin.Context) {
		// 這裡是 RDP 操作，可以記錄特定的 PEP 事件
		ip := c.ClientIP()
		user := getUserFromJWT(c) // 根據需求設定用戶
		logPEPEvent("RDP Connection", user, ip, "Success")
		view.RdpProxy(c)
	})

	view.ProxyRegisterRoutes(r)
	view.HTMLtRoutes(r)
	view.WebauthRegisterRoutes(r)
	view.SSHRoutes(r)

	// 啟動伺服器，改成 HTTPS
	certFile := "./cert/server.crt"
	keyFile := "./cert/private.key"

	err := r.RunTLS(":8080", certFile, keyFile)
	if err != nil {
		log.Fatal("Failed to start HTTPS server : ", err)
	}

}
