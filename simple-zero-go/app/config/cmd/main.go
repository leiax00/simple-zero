package main

import (
	"flag"
	"github.com/gin-gonic/gin"
	"github.com/go-kratos/kratos/contrib/config/etcd/v2"
	"github.com/go-kratos/kratos/v2/config"
	"github.com/go-kratos/kratos/v2/config/file"
	"github.com/leiax00/simple-zero/app/config/internal/conf"
	"github.com/leiax00/simple-zero/app/config/internal/server"
	logger2 "github.com/leiax00/simple-zero/pkg/logger"
	"github.com/samber/lo"
	clientV3 "go.etcd.io/etcd/client/v3"
	"go.uber.org/zap"
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
	// cat confi_file | etcdctl put <key> 写入配置文件
	flag.StringVar(&cfg.etcd, "etcd", "", "etcd server, eg: ip1:port;ip2:port")
	//flag.StringVar(&cfg.etcd, "etcd", "10.1.0.3:2379;10.1.0.3:2381;10.1.0.3:2383", "etcd server, eg: ip1:port;ip2:port")
}

func newApp(conf *conf.Config, logger *logger2.Logger, httpServer *server.HttpServer) *App {
	app := NewApp(conf, logger)
	app.RegisterServ(httpServer)
	return app
}

func loadConf(client *clientV3.Client) *conf.Config {
	var sourceList []config.Source
	sourceList = append(sourceList, file.NewSource(cfg.conf))
	if lo.IsNotEmpty(client) {
		source, err := etcd.New(client, etcd.WithPath("/app-config/configuration"), etcd.WithPrefix(true))
		if err == nil {
			sourceList = append(sourceList, source)
		}
	}

	c := config.New(
		config.WithSource(sourceList...),
	)
	//defer func(c config.Config) {
	//	_ = c.Close()
	//}(c)

	if err := c.Load(); err != nil {
		panic(err)
	}

	var bc conf.Config
	if err := c.Scan(&bc); err != nil {
		panic(err)
	}
	return &bc
}

func main() {
	flag.Parse()
	gin.SetMode(gin.ReleaseMode)

	var client *clientV3.Client
	if lo.IsNotEmpty(cfg.etcd) {
		client = server.NewEtcdClient(strings.Split(cfg.etcd, ";"))
	}

	c := loadConf(client)
	logger := logger2.NewLogger(c.Log)
	logger.Info("", zap.Any("config", c))
	app := wireApp(c, logger)
	if err := app.Run(); err != nil {
		logger.Fatal(err.Error())
	}
}
