package biz

import (
	"context"
	"encoding/base64"
	api "github.com/leiax00/simple-zero/api/config/v1"
	"github.com/leiax00/simple-zero/pkg/logger"
	clientV3 "go.etcd.io/etcd/client/v3"
)

type ConfigRepo interface {
	GetProp(ctx context.Context, key string, opts ...clientV3.OpOption) (*clientV3.GetResponse, error)
}

type ConfigUseCase struct {
	repo ConfigRepo
	log  *logger.Logger
}

func NewConfiUseCase(repo ConfigRepo, logger *logger.Logger) *ConfigUseCase {
	return &ConfigUseCase{
		repo: repo,
		log:  logger,
	}
}

func (uc *ConfigUseCase) GetProp(ctx context.Context, cond *api.PropCond) ([]*api.KvObj, error) {
	decodeString, err := base64.StdEncoding.DecodeString(cond.Key)
	if err != nil {
		return nil, err
	}
	opts := []clientV3.OpOption{clientV3.WithPrefix()}
	resp, err := uc.repo.GetProp(ctx, string(decodeString), opts...)
	if err != nil {
		return nil, err
	}
	var kvList []*api.KvObj
	for _, kv := range resp.Kvs {
		kvList = append(kvList, &api.KvObj{
			Key:   string(kv.Key),
			Value: string(kv.Value),
		})
	}
	return kvList, nil
}
