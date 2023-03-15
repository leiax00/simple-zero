// Code generated by Wire. DO NOT EDIT.

//go:generate go run github.com/google/wire/cmd/wire
//go:build !wireinject
// +build !wireinject

package main

import (
	"github.com/leiax00/simple-zero/app/config/internal/biz"
	"github.com/leiax00/simple-zero/app/config/internal/conf"
	"github.com/leiax00/simple-zero/app/config/internal/data"
	"github.com/leiax00/simple-zero/app/config/internal/server"
	"github.com/leiax00/simple-zero/app/config/internal/service"
	"github.com/leiax00/simple-zero/pkg/logger"
)

// Injectors from wire.go:

func initApp(etcdAddrList []string, localConfPath string) *App {
	client := server.NewEtcdClient(etcdAddrList)
	config := conf.LoadConf(client, localConfPath)
	logConf := conf.GetLogConf(config)
	loggerLogger := logger.NewLogger(logConf)
	configRepo := data.NewConfigRepo(client)
	configUseCase := biz.NewConfiUseCase(configRepo, loggerLogger)
	configService := service.NewConfigService(configUseCase)
	httpServer := server.NewHttpServer(loggerLogger, configService)
	registry := server.NewEtcdRegister(client)
	app := newApp(config, loggerLogger, httpServer, registry)
	return app
}
