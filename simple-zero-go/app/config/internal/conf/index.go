package conf

import (
	"github.com/go-kratos/kratos/contrib/config/etcd/v2"
	"github.com/go-kratos/kratos/v2/config"
	"github.com/go-kratos/kratos/v2/config/file"
	"github.com/google/wire"
	"github.com/leiax00/simple-zero/pkg/logger"
	"github.com/samber/lo"
	clientV3 "go.etcd.io/etcd/client/v3"
)

var ProvideSet = wire.NewSet(
	LoadConf,
	GetLogConf,
)

func GetLogConf(c *Config) *logger.LogConf {
	return c.Log
}

func LoadConf(client *clientV3.Client, localConfPath string) *Config {
	var sourceList []config.Source
	sourceList = append(sourceList, file.NewSource(localConfPath))
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

	var bc Config
	if err := c.Scan(&bc); err != nil {
		panic(err)
	}
	return &bc
}
