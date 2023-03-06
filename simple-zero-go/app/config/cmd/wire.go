//go:build wireinject
// +build wireinject

package main

import (
	"github.com/leiax00/simple-zero/app/config/internal/conf"
	"github.com/leiax00/simple-zero/app/config/internal/server"
	logger2 "github.com/leiax00/simple-zero/pkg/logger"
)
import "github.com/google/wire"

func wireApp(*conf.Config, *logger2.Logger) *App {
	panic(wire.Build(server.ProvideSet, newApp))
}
