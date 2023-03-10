package data

import (
	"context"
	"github.com/leiax00/simple-zero/app/config/internal/biz"
	clientV3 "go.etcd.io/etcd/client/v3"
)

type configRepo struct {
	etcd *clientV3.Client
}

func NewConfigRepo(etcd *clientV3.Client) biz.ConfigRepo {
	return &configRepo{etcd}
}

func (cRepo *configRepo) GetProp(ctx context.Context, key string, opts ...clientV3.OpOption) (*clientV3.GetResponse, error) {
	return cRepo.etcd.Get(ctx, key, opts...)
}
