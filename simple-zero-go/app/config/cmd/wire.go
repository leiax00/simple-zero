//go:build wireinject
// +build wireinject

package main

import (
	"github.com/leiax00/simple-zero/app/config/internal/conf"
	"github.com/leiax00/simple-zero/app/config/internal/server"
	"github.com/leiax00/simple-zero/app/config/internal/service"
	logger2 "github.com/leiax00/simple-zero/pkg/logger"
)
import "github.com/google/wire"

func wireApp(etcdAddrList []string, localConfPath string) *App {
	panic(wire.Build(
		server.ProvideSet,
		conf.ProvideSet,
		logger2.ProvideSet,
		service.ProviderSet,
		newApp,
	))
}
