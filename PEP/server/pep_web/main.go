package main

import (
    "log"
    "io/ioutil"
    "net/http"
    "fmt"
    "github.com/gin-gonic/gin"
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)


type ProxyHost struct {
    ID          uint      `gorm:"primaryKey"`
    Source      string    `json:"source"`
    Destination string    `json:"destination"`
    Port        string    `json:"port"`
    Description string    `json:"description"`
}

func (ProxyHost) TableName() string {
    return "proxy_hosts"
}

var db *gorm.DB


func main() {
    var err error
    dsn := "web:password@tcp(127.0.0.1:3306)/PROXYDB"
   
    // 初始化 GORM 和資料庫連接
    db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        log.Fatal(err)
    }

    // 自動遷移資料庫結構
    db.AutoMigrate(&ProxyHost{})

    fmt.Println("Successfully connected to the database!")

    r := gin.Default()
    r.LoadHTMLGlob("templates/*")
    r.Static("/static", "./static")

    r.GET("/", func(c *gin.Context) {
        var proxyHosts []ProxyHost
        db.Find(&proxyHosts)
        c.HTML(http.StatusOK, "index.html", gin.H{
            "proxyHosts": proxyHosts,
        })
    })

    r.POST("/add-proxy-host", func(c *gin.Context) {
        fmt.Println("HI")
        var newProxyHost ProxyHost
        if err := c.BindJSON(&newProxyHost); err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"success": false, "error": err.Error()})
            return
        }

        // 打印接收到的數據
        fmt.Printf("Received data: %+v\n", newProxyHost)


        db.Create(&newProxyHost)
        c.JSON(http.StatusOK, gin.H{"success": true, "proxyHost": newProxyHost})
    })

    r.DELETE("/delete-proxy-host/:id", func(c *gin.Context) {
        id := c.Param("id")
        var proxyHost ProxyHost
        if err := db.First(&proxyHost, id).Error; err != nil {
            c.JSON(http.StatusBadRequest, gin.H{"success": false, "error": "Record not found"})
            return
        }

        db.Delete(&proxyHost)
        c.JSON(http.StatusOK, gin.H{"success": true, "message": "Record deleted"})
    })

    r.GET("/logs", func(c *gin.Context){
        data,err := ioutil.ReadFile("../index/app.log")
        if err != nil {
            c.String(http.StatusInternalServerError, "無法讀取日誌文件")
            return
        }
        c.HTML(http.StatusOK, "log.html", gin.H{
            "log": string(data),
        })
    })
    r.Run(":8080") // Listen and serve on 0.0.0.0:8080
}
