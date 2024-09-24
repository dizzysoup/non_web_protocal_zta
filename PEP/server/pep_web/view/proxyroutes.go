package view

import (
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/gin-gonic/gin"
	//"gorm.io/gorm"
)

type ProxyHost struct {
	ID          uint   `gorm:"primaryKey"`
	Source      string `json:"source"`
	Destination string `json:"destination"`
	Port        string `json:"port"`
	Description string `json:"description"`
}

func ProxyRegisterRoutes(r *gin.Engine) {

	proxyGrop := r.Group("/proxy")

	proxyGrop.GET("/", func(c *gin.Context) {
		var proxyHosts []ProxyHost
		//	db.Find(&proxyHosts)
		c.HTML(http.StatusOK, "index.html", gin.H{
			"proxyHosts": proxyHosts,
		})
	})

	proxyGrop.POST("/add-proxy-host", func(c *gin.Context) {
		var newProxyHost ProxyHost
		if err := c.BindJSON(&newProxyHost); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"success": false, "error": err.Error()})
			return
		}

		// 打印接收到的數據
		fmt.Printf("Received data: %+v\n", newProxyHost)

		//	db.Create(&newProxyHost)
		c.JSON(http.StatusOK, gin.H{"success": true, "proxyHost": newProxyHost})
	})

	/*
		proxyGrop.DELETE("/delete-proxy-host/:id", func(c *gin.Context) {
			id := c.Param("id")
			var proxyHost ProxyHost
			/*
			if err := db.First(&proxyHost, id).Error; err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"success": false, "error": "Record not found"})
				return
			}

			db.Delete(&proxyHost)

			c.JSON(http.StatusOK, gin.H{"success": true, "message": "Record deleted"})
		})
	*/
	proxyGrop.GET("/logs", func(c *gin.Context) {
		data, err := ioutil.ReadFile("../index/app.log")
		if err != nil {
			c.String(http.StatusInternalServerError, "無法讀取日誌文件")
			return
		}
		c.HTML(http.StatusOK, "log.html", gin.H{
			"log": string(data),
		})
	})
}
