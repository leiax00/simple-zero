package main

import (
	"context"
	"errors"
	"github.com/go-kratos/kratos/contrib/registry/etcd/v2"
	"github.com/go-kratos/kratos/v2/registry"
	"github.com/go-kratos/kratos/v2/transport"
	"github.com/google/uuid"
	"github.com/leiax00/simple-zero/app/config/internal/conf"
	"github.com/leiax00/simple-zero/app/config/internal/server"
	logger2 "github.com/leiax00/simple-zero/pkg/logger"
	"golang.org/x/sync/errgroup"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

type App struct {
	conf     *conf.Config
	log      *logger2.Logger
	ctx      context.Context
	cancel   func()
	servers  []server.Server
	register registry.Registrar
	instance *registry.ServiceInstance
}

func NewApp(conf *conf.Config, logger *logger2.Logger, register *etcd.Registry) *App {
	ctx, cancel := context.WithCancel(context.Background())
	return &App{
		conf:     conf,
		log:      logger,
		ctx:      ctx,
		cancel:   cancel,
		register: register,
	}
}

func (app *App) RegisterServ(serv server.Server) {
	if app.servers == nil {
		app.servers = []server.Server{}
	}
	app.servers = append(app.servers, serv)
}

func (app *App) shutdownServ(serv server.Server) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	return serv.Stop(ctx)
}

func (app *App) Run() error {
	ctx := NewContext(app.ctx, app)
	errG, ctx := errgroup.WithContext(ctx)
	wg := sync.WaitGroup{}

	for _, serv := range app.servers {
		serv := serv
		errG.Go(func() error {
			<-ctx.Done()
			sctx, cancel := context.WithTimeout(NewContext(context.Background(), app), 5*time.Second)
			defer cancel()
			return serv.Stop(sctx)
		})
		wg.Add(1)
		errG.Go(func() error {
			wg.Done()
			return serv.Start(context.Background())
		})
	}
	wg.Wait()
	instance, err := app.buildInstance()
	if err != nil {
		return err
	}
	if app.register != nil {
		rCtx, rCancel := context.WithTimeout(app.ctx, 10*time.Second)
		defer rCancel()
		if err := app.register.Register(rCtx, instance); err != nil {
			return err
		}
		app.instance = instance
	}

	c := make(chan os.Signal, 1)
	signal.Notify(c, []os.Signal{syscall.SIGTERM, syscall.SIGQUIT, syscall.SIGINT}...)
	errG.Go(func() error {
		for {
			select {
			case <-ctx.Done():
				return ctx.Err()
			case <-c:
				return app.Stop()
			}
		}
	})
	if err := errG.Wait(); err != nil && !errors.Is(err, context.Canceled) {
		return err
	}
	return nil
}

func (app *App) Stop() error {
	if app.register != nil && app.instance != nil {
		ctx, cancel := context.WithTimeout(app.ctx, 10*time.Second)
		defer cancel()
		if err := app.register.Deregister(ctx, app.instance); err != nil {
			return err
		}
	}
	if app.cancel != nil {
		app.cancel()
	}
	return nil
}

func (app *App) buildInstance() (*registry.ServiceInstance, error) {
	endpoints := make([]string, 0)
	for _, srv := range app.servers {
		if r, ok := srv.(transport.Endpointer); ok {
			e, err := r.Endpoint()
			if err != nil {
				return nil, err
			}
			endpoints = append(endpoints, e.String())
		}
	}
	r := &registry.ServiceInstance{
		Name:      Name,
		Version:   Version,
		Metadata:  make(map[string]string),
		Endpoints: endpoints,
	}
	if id, err := uuid.NewUUID(); err == nil {
		r.ID = id.String()
	}
	return r, nil
}

type appKey struct{}

func NewContext(ctx context.Context, app *App) context.Context {
	return context.WithValue(ctx, appKey{}, app)
}
