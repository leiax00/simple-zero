// Code generated by Wire. DO NOT EDIT.

//go:generate go run github.com/google/wire/cmd/wire
//go:build !wireinject
// +build !wireinject

package main

import (
	"github.com/simple-zero/app/configuration/service/internal/conf"
	"github.com/simple-zero/app/configuration/service/internal/server"
	"github.com/simple-zero/pkg/logger"
)

// Injectors from wire.go:

func wireApp(config *conf.Config, loggerLogger *logger.Logger) *App {
	httpServer := server.NewHttpServer(loggerLogger)
	app := newApp(config, loggerLogger, httpServer)
	return app
}