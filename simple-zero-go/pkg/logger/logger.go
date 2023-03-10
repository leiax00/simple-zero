package logger

import (
	kratoszap "github.com/go-kratos/kratos/contrib/log/zap/v2"
	"github.com/go-kratos/kratos/v2/log"
	"github.com/google/wire"
	"github.com/natefinch/lumberjack"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

var ProvideSet = wire.NewSet(NewLogger)

type Logger struct {
	*zap.Logger
	Sugar *zap.SugaredLogger
}

func (l *Logger) Log(level log.Level, kvs ...interface{}) error {
	var fn func(msg string, fields ...zap.Field)
	if level == log.LevelFatal {
		fn = l.Fatal
	} else if level == log.LevelWarn {
		fn = l.Warn
	} else if level == log.LevelError {
		fn = l.Error
	} else if level == log.LevelDebug {
		fn = l.Debug
	} else {
		fn = l.Info
	}
	fn("kratos", zap.Any("kratos", kvs))
	return nil
}

func NewLogger(conf *LogConf) *Logger {
	writeSyncer := getLogWriter(conf)
	encoder := getEncoder()
	core := zapcore.NewCore(encoder, writeSyncer, zapcore.DebugLevel)
	logger := zap.New(core, zap.AddCallerSkip(2))

	log.SetLogger(kratoszap.NewLogger(logger)) // 设置全局的kratos日志对象
	return &Logger{
		Logger: logger,
		Sugar:  logger.Sugar(),
	}
}

func getEncoder() zapcore.Encoder {
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	encoderConfig.TimeKey = "time"
	encoderConfig.EncodeLevel = zapcore.CapitalLevelEncoder
	encoderConfig.EncodeDuration = zapcore.SecondsDurationEncoder
	encoderConfig.EncodeCaller = zapcore.ShortCallerEncoder
	encoder := zapcore.NewJSONEncoder(encoderConfig)
	return encoder
}

func getLogWriter(conf *LogConf) zapcore.WriteSyncer {
	lumberJackLogger := &lumberjack.Logger{
		Filename:   conf.LogFile,
		MaxSize:    int(conf.MaxSize),
		MaxBackups: int(conf.MaxBackup),
		MaxAge:     int(conf.MaxAge),
		Compress:   false,
	}
	return zapcore.AddSync(lumberJackLogger)
}
