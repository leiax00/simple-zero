package service

import (
	"github.com/google/wire"
	"github.com/leiax00/simple-zero/app/config/internal/biz"
)

var ProviderSet = wire.NewSet(NewConfigService)

func NewConfigService(uc *biz.ConfigUseCase) *ConfigService {
	return &ConfigService{uc}
}
