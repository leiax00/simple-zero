package main

import (
	"fmt"
	"github.com/samber/lo"
	"github.com/simple-zero/app/configuration/service/internal/server"
	logger2 "github.com/simple-zero/pkg/logger"
	"log"
)

func main() {
	fmt.Println(lo.If(true, 1).Else(2))
	//gin.SetMode(gin.ReleaseMode)
	logger := logger2.NewLogger()
	app := NewApp()
	app.RegisterServ(server.NewHttpServer(logger))
	if err := app.Run(); err != nil {
		log.Fatal(err)
	}
}
