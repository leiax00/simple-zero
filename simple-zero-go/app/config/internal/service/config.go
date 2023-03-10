package service

import (
	"context"
	api "github.com/leiax00/simple-zero/api/config/v1"
)

func (c *ConfigService) GetProp(ctx context.Context, cond *api.PropCond) (*api.Prop, error) {
	return &api.Prop{
		Result: cond.Key,
	}, nil
}
