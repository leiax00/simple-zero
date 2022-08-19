package server

import (
	"context"
	"github.com/google/wire"
	"net/http"
)

type Server interface {
	Start(context.Context) error
	Stop(context.Context) error
}

type HttpServer struct {
	http.Server
	BaseContext context.Context
}

func (h *HttpServer) Start(ctx context.Context) error {
	h.BaseContext = ctx
	return h.ListenAndServe()
}

func (h *HttpServer) Stop(ctx context.Context) error {
	return h.Shutdown(ctx)
}

var ProvideSet = wire.NewSet(
	NewHttpServer,
)
