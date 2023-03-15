package data

import (
	"context"
	clientV3 "go.etcd.io/etcd/client/v3"
)

type configRepo struct {
	etcd *clientV3.Client
}

func (cRepo *configRepo) GetProp(ctx context.Context, key string, opts ...clientV3.OpOption) (*clientV3.GetResponse, error) {
	return cRepo.etcd.Get(ctx, key, opts...)
}
