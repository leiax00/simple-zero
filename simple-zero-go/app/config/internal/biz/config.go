package biz

import (
	"context"
	"encoding/base64"
	api "github.com/leiax00/simple-zero/api/config/v1"
	"github.com/leiax00/simple-zero/pkg/logger"
	"github.com/samber/lo"
	clientV3 "go.etcd.io/etcd/client/v3"
)

type ConfigRepo interface {
	GetProp(ctx context.Context, key string, opts ...clientV3.OpOption) (*clientV3.GetResponse, error)
}

type ConfigUseCase struct {
	repo ConfigRepo
	log  *logger.Logger
}

func (uc *ConfigUseCase) GetProp(ctx context.Context, cond *api.PropCond) ([]*api.KvObj, error) {
	decodeString, err := base64.StdEncoding.DecodeString(cond.Key)
	if err != nil {
		return nil, err
	}
	var opts []clientV3.OpOption
	if cond.Prefix {
		opts = append(opts, clientV3.WithPrefix())
	}
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
	return lo.If(len(kvList) == 0, []*api.KvObj{}).Else(kvList), nil
}
