package main

import (
	"flag"
	"github.com/gin-gonic/gin"
	"github.com/go-kratos/kratos/contrib/registry/etcd/v2"
	"github.com/leiax00/simple-zero/app/config/internal/conf"
	"github.com/leiax00/simple-zero/app/config/internal/server"
	logger2 "github.com/leiax00/simple-zero/pkg/logger"
	"github.com/samber/lo"
	"strings"
)

// go build -ldflags "-X main.Version=x.y.z"
var (
	// Name is the name of the compiled software.
	Name string = "sz-novel"
	// Version is the version of the compiled software.
	Version string
	// conf is the config flag.
	cfg = struct {
		conf string
		etcd string
	}{}
)

func init() {
	flag.StringVar(&cfg.conf, "conf", "./app/config/configs", "config path, eg: -conf config.yaml")
	flag.StringVar(&cfg.etcd, "etcd", "10.1.0.3:2379;10.1.0.3:2381;10.1.0.3:2383", "etcd server, eg: ip1:port;ip2:port")
}

func newApp(conf *conf.Config, logger *logger2.Logger, httpServer *server.HttpServer, register *etcd.Registry) *App {
	app := NewApp(conf, logger, register)
	app.RegisterServ(httpServer)
	if err := app.Run(); err != nil {
		logger.Fatal(err.Error())
	}
	return app
}

func main() {
	flag.Parse()
	gin.SetMode(gin.ReleaseMode)

	if lo.IsEmpty(cfg.etcd) {
		panic("Failed to find ETCD config, please set it!")
	}
	initApp(strings.Split(cfg.etcd, ";"), cfg.conf)
}
