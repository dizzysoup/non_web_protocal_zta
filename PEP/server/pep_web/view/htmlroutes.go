package view

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func HTMLtRoutes(r *gin.Engine) {
	// 根路徑，顯示首頁 Home screen.html
	r.GET("/", func(c *gin.Context) {
		var proxyHosts []ProxyHost

		c.HTML(http.StatusOK, "Home screen.html", gin.H{
			"proxyHosts": proxyHosts,
		})
	})

	// 註冊路徑，顯示 register.html
	r.GET("/register", func(c *gin.Context) {
		c.HTML(http.StatusOK, "register.html", nil)
	})
	r.POST("/register/begin", BeginRegistration)
	r.POST("/register/complete", CompleteRegistration)

	// 註冊路徑，顯示 login.html
	r.GET("/login", func(c *gin.Context) {
		c.HTML(http.StatusOK, "login.html", nil)
	})
	r.POST("/login/begin", BeginRegistration)
	r.POST("/login/complete", CompleteRegistration)

}
