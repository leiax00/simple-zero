package data

import (
	"context"
	"encoding/json"
	"fmt"
	api "github.com/leiax00/simple-zero/api/config/v1"
	clientV3 "go.etcd.io/etcd/client/v3"
	"time"
)

type configRepo struct {
	etcd *clientV3.Client
}

func (cRepo *configRepo) SetUIServe(ctx context.Context, serve *api.UIServe) error {
	key := fmt.Sprintf("%s/%s", "app/ui/serve", serve.Name)
	c, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()
	bytes, err := json.Marshal(serve)
	if err != nil {
		return err
	}

	_, err = cRepo.etcd.Put(c, key, string(bytes))
	if err != nil {
		return err
	}
	return err
}

func (cRepo *configRepo) SetUIMenu(ctx context.Context, config *api.UIConfig) error {
	key := fmt.Sprintf("%s/%s", "app/ui/menu", config.Serve.Name)
	c, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()
	bytes, err := json.Marshal(config.Menus)
	if err != nil {
		return err
	}

	_, err = cRepo.etcd.Put(c, key, string(bytes))
	if err != nil {
		return err
	}
	return err
}

func (cRepo *configRepo) GetProp(ctx context.Context, key string, opts ...clientV3.OpOption) (*clientV3.GetResponse, error) {
	return cRepo.etcd.Get(ctx, key, opts...)
}
