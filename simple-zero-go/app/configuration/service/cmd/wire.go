//go:build wireinject
// +build wireinject

package main

import (
	"github.com/simple-zero/app/configuration/service/internal/conf"
	"github.com/simple-zero/app/configuration/service/internal/server"
	logger2 "github.com/simple-zero/pkg/logger"
)
import "github.com/google/wire"

func wireApp(*conf.Config, *logger2.Logger) *App {
	panic(wire.Build(server.ProvideSet, newApp))
}
