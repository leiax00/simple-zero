package main

import (
	"context"
	"errors"
	"github.com/simple-zero/app/configuration/service/internal/server"
	"golang.org/x/sync/errgroup"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

type App struct {
	ctx     context.Context
	cancel  func()
	servers []server.Server
}

func NewApp() *App {
	ctx, cancel := context.WithCancel(context.Background())
	return &App{ctx: ctx, cancel: cancel}
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
	}
	if err := errG.Wait(); err != nil && !errors.Is(err, context.Canceled) {
		return err
	}
	return nil
}

func (app *App) Stop() error {
	if app.cancel != nil {
		app.cancel()
	}
	return nil
}

type appKey struct{}

func NewContext(ctx context.Context, app *App) context.Context {
	return context.WithValue(ctx, appKey{}, app)
}
