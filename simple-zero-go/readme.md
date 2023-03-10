# 使用教程
> 本项目是golang项目 <br>
> 基于 `kratos` + `gin` 进行开发 <br>
> 因此在开发过程中需要安装相关的依赖
## 文档列表
[kratos文档: 点击参考: https://go-kratos.dev/docs/](https://go-kratos.dev/docs/) <br>
[gin文档: 点击参考: https://gin-gonic.com/zh-cn/docs/](https://gin-gonic.com/zh-cn/docs/) <br>

## 前置安装
1. [go -> 中文社区下载](https://studygolang.com/dl)
2. [protoc](https://github.com/protocolbuffers/protobuf/releases)
3. [protoc-gen-go](https://github.com/protocolbuffers/protobuf-go/releases)
4. [protoc-gen-gin: `go install github.com/leiax00/protoc-gen-gin@latest`](https://github.com/leiax00/protoc-gen-gin)
5. [protoc-go-inject-tag: `go install github.com/favadi/protoc-go-inject-tag@latest`](https://github.com/favadi/protoc-go-inject-tag)
6. [kratos cli工具: `go install github.com/go-kratos/kratos/cmd/kratos/v2@latest`](https://go-kratos.dev/docs/getting-started/usage#%E5%AE%89%E8%A3%85)
7. wire -- `go install github.com/google/wire/cmd/wire@latest`

## 常用的命令
### kratos cli
1. 通过 kratos 命令创建项目模板: `kratos new helloworld [-r 自定义模板git仓库] [-b 指定的分支] [--nomod]`
    ```shell
    # 使用 --nomod 添加服务，共用 go.mod ，大仓模式
    kratos new helloworld
    cd helloworld
    kratos new app/user --nomod
    ```
2. 添加 Proto 文件: `kratos proto add api/helloworld/v1/demo.proto`
3. 生成 Proto客户端代码: `kratos proto client api/helloworld/v1/demo.proto`
4. 生成 Proto服务端代码: `kratos proto server api/helloworld/v1/demo.proto -t internal/service`
5. 运行项目: `kratos run `
6. 工具升级: `kratos upgrade `

### protobuf
```shell
# common.proto
protoc -I api --go_out=api api/common/v1/common.proto

# simple-zero-go/api/config/v1/api.proto http
protoc --proto_path=./third_party -I ./api --go_out ./api --go_opt=paths=source_relative --gin_out ./api --gin_opt=paths=source_relative api/config/v1/api.proto

# 生成自定义tag
protoc-go-inject-tag -input="*.pb.go"
```

### 其他
1. 代码生成, 包括所有proto源码、wire等: `go generate ./...`
2. 通过 `protoc-gen-gin`生成http服务
   ```shell
   protoc -I ./example/api \
     --go_out ./example/api --go_opt=paths=source_relative \
     --gin_out ./example/api --gin_opt=paths=source_relative \
     example/api/product/app/v1/v1.proto
   
   protoc --proto_path=./third_party -I ./api --go_out ./api --go_opt=paths=source_relative --gin_out ./api --gin_opt=paths=source_relative api/config/v1/api.proto
   ```
3. wire生成, 在wire.go目录执行命令: `wire`
   ```go
   // wire.go文件模板
   
   //go:build wireinject
   // +build wireinject
   
   package main
   
   import (
      "github.com/leiax00/simple-zero/app/config/internal/conf"
      "github.com/leiax00/simple-zero/app/config/internal/server"
      logger2 "github.com/leiax00/simple-zero/pkg/logger"
   )
   import "github.com/google/wire"
   
   func wireApp(*conf.Config, *logger2.Logger) *App {
      panic(wire.Build(server.ProvideSet, newApp))
   }
   
   ```
