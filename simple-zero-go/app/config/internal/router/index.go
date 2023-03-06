package router

import (
	"github.com/gin-gonic/gin"
)

func RegisterRoutesTo(router *gin.Engine) {
	registerBaseRoutes(router)
}
