package data

import "github.com/google/wire"

var ProvideSet = wire.NewSet(NewConfigRepo)
