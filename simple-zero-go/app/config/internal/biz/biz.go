package biz

import "github.com/google/wire"

var ProvideSet = wire.NewSet(NewConfiUseCase)
