package view

import (
	"bytes"
	"crypto/tls"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/go-webauthn/webauthn/webauthn"
	"github.com/golang-jwt/jwt/v5"
)

var (
	web *webauthn.WebAuthn
	err error
)

func WebauthRegisterRoutes(r *gin.Engine) {

	web, err = webauthn.New(&webauthn.Config{
		RPDisplayName: "Foobar Corp.", // Display Name for your site
		RPID:          "localhost",
		RPOrigins:     []string{"http://localhost:8080"}, // Generally the domain name for your site
	})

	if err != nil {
		log.Fatalf("failed to initialize webauthn: %v", err)
	}

	r.GET("/", func(c *gin.Context) {
		var proxyHosts []ProxyHost

		c.HTML(http.StatusOK, "register.html", gin.H{
			"proxyHosts": proxyHosts,
		})
	})

	r.POST("/register/begin", BeginRegistration)
	r.POST("/register/complete", CompleteRegistration)
}

func BeginRegistration(c *gin.Context) {
	var data map[string]interface{}
	if err := c.BindJSON(&data); err != nil || data["username"] == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid input, username is required"})
		return
	}
	url := "https://de.yuntech.poc.com:3443/fido2/register/begin"
	method := "POST"
	payload, _ := json.Marshal(data)
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{Transport: tr}
	req, err := http.NewRequest(method, url, bytes.NewBuffer(payload))
	if err != nil {
		fmt.Println(err)
		return
	}
	req.Header.Add("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Failed to read response")
		return
	}
	fmt.Println(string(body))
	c.Data(http.StatusOK, "application/json", body)
}

func CompleteRegistration(c *gin.Context) {
	var data map[string]interface{}
	if err := c.BindJSON(&data); err != nil {
		fmt.Println(err.Error())
		return
	}
	if tokenMap, ok := data["credential"].(map[string]interface{}); ok {
		// 將 tokenMap 的內容合併到頂層 data 中
		for key, value := range tokenMap {
			data[key] = value
		}
		// 移除 token 層
		delete(data, "credential")
	}
	fmt.Println(data)
	claims := jwt.MapClaims{}
	for key, value := range data {
		claims[key] = value
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	tokenString, err := token.SignedString([]byte("Jf9l1Kz3t5qDs8oG6jP7U3v0XwS9b4CkNzLmQxVc7rTfYnHaUv"))
	if err != nil {
		fmt.Println(err.Error())
	}

	fmt.Println(tokenString)

	// post to de
	url := "https://de.yuntech.poc.com:3443/fido2/register/complete"
	method := "POST"

	tokenPayload := map[string]string{
		"token": tokenString,
	}

	payload, _ := json.Marshal(tokenPayload)
	tr := &http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
	}
	client := &http.Client{Transport: tr}
	req, err := http.NewRequest(method, url, bytes.NewBuffer(payload))
	if err != nil {
		fmt.Println(err)
		return
	}
	req.Header.Add("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Failed to read response : begin/complete")
		return
	}
	fmt.Println(string(body))
	c.Data(http.StatusOK, "application/json", body)
}
