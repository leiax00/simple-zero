package server

import (
	"context"
	"github.com/gin-gonic/gin"
	"github.com/simple-zero/app/configuration/service/internal/router"
)

func NewHttpServer() Server {
	engine := gin.New()
	router.RegisterRoutesTo(engine)
	h := &HttpServer{BaseContext: context.Background()}
	h.Addr = ":8080"
	h.Handler = engine
	return h
}
