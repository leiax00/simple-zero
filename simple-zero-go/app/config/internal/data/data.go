package data

import (
	"github.com/google/wire"
	"github.com/leiax00/simple-zero/app/config/internal/biz"
	clientV3 "go.etcd.io/etcd/client/v3"
)

var ProvideSet = wire.NewSet(NewConfigRepo)

func NewConfigRepo(etcd *clientV3.Client) biz.ConfigRepo {
	return &configRepo{etcd}
}
