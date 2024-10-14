package view

import (
	"agweb/freerdp"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
)

var upgrade = websocket.Upgrader{CheckOrigin: func(r *http.Request) bool { return true }}

func RdpProxy(ctx *gin.Context) {
	proto := ctx.Request.Header.Get("Sec-Websocket-Protocol")

	ws, err := upgrade.Upgrade(ctx.Writer, ctx.Request, http.Header{
		"Sec-Websocket-Protocol": {proto},
	})
	if err != nil {
		panic(err)
	}

	client := freerdp.NewClient("192.168.50.83",
		"Administrator", "1qaz@WSX3edc")

	if err := client.Connect(); err != nil {
		panic(err)
	}
	defer client.DisConnect()

	go func() {
		if err := client.Start(); err != nil {
			panic(err)
		}
	}()

	go func() {
		for {
			var msg freerdp.Message
			if err := ws.ReadJSON(&msg); err != nil {
				fmt.Println("read from websocket fail:", err)
				client.DisConnect()
				break
			} else {
				if msg.Mouse != nil {
					client.ProcessMouseEvent(msg.Mouse)
				} else if msg.Keyboard != nil {
					client.ProcessKeyboardEvent(msg.Keyboard)
				}
			}
		}
	}()

	for {
		if msg, ok := client.Data(); !ok {
			fmt.Println("read from dataChan failed:", ok)
			break
		} else if err := ws.WriteJSON(&msg); err != nil {
			fmt.Println("write to websocket failed:", err)
			break
		} else {

		}
	}
}
