package service

import (
	"github.com/google/wire"
	clientV3 "go.etcd.io/etcd/client/v3"
)

var ProviderSet = wire.NewSet(NewConfigService)

type ConfigService struct {
	etcd *clientV3.Client
}

func NewConfigService(etcd *clientV3.Client) *ConfigService {
	return &ConfigService{etcd}
}
