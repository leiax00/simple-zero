package main

import (
	"flag"
	"github.com/gin-gonic/gin"
	"github.com/leiax00/simple-zero/app/config/internal/conf"
	"github.com/leiax00/simple-zero/app/config/internal/server"
	logger2 "github.com/leiax00/simple-zero/pkg/logger"
	"github.com/samber/lo"
	"os"
	"strings"
)

// go build -ldflags "-X main.Version=x.y.z"
var (
	// Name is the name of the compiled software.
	Name string
	// Version is the version of the compiled software.
	Version string
	// conf is the config flag.
	cfg = struct {
		conf string
		etcd string
	}{}

	id, _ = os.Hostname()
)

func init() {
	flag.StringVar(&cfg.conf, "conf", "./app/config/configs", "config path, eg: -conf config.yaml")
	flag.StringVar(&cfg.etcd, "etcd", "10.1.0.3:2379;10.1.0.3:2381;10.1.0.3:2383", "etcd server, eg: ip1:port;ip2:port")
}

func newApp(conf *conf.Config, logger *logger2.Logger, httpServer *server.HttpServer) *App {
	app := NewApp(conf, logger)
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
	wireApp(strings.Split(cfg.etcd, ";"), cfg.conf)
}
