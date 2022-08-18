package main

import (
	"fmt"
	"github.com/samber/lo"
	"github.com/simple-zero/app/configuration/service/internal/server"
	"log"
)

func main() {
	fmt.Println(lo.If(true, 1).Else(2))
	//gin.SetMode(gin.ReleaseMode)
	app := NewApp()
	app.RegisterServ(server.NewHttpServer())
	if err := app.Run(); err != nil {
		log.Fatal(err)
	}
}
