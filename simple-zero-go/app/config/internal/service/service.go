package service

import "github.com/google/wire"

var ProviderSet = wire.NewSet(NewConfigService)

type ConfigService struct{}

func NewConfigService() *ConfigService {
	return &ConfigService{}
}
