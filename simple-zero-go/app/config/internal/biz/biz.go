package biz

import (
	"github.com/google/wire"
	"github.com/leiax00/simple-zero/pkg/logger"
)

var ProvideSet = wire.NewSet(NewConfiUseCase)

func NewConfiUseCase(repo ConfigRepo, logger *logger.Logger) *ConfigUseCase {
	return &ConfigUseCase{
		repo: repo,
		log:  logger,
	}
}
