package service

import (
	"context"
	api "github.com/leiax00/simple-zero/api/config/v1"
)

func (c *ConfigService) GetProp(ctx context.Context, cond *api.PropCond) (*api.PropReply, error) {
	kvs, err := c.uc.GetProp(ctx, cond)
	if err != nil {
		return nil, err
	}
	return &api.PropReply{Kvs: kvs}, nil
}
