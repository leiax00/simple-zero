# simple zero ui

> ui项目根路径

## 项目构建

1. 安装依赖包: `pnpm i`
2. 编译指定模块, 如:
    ```text
    main:        pnpm -F sz-main build:main
    novel:       pnpm -F sz-novel build:novel
    tools:       pnpm -F sz-tools build:tools
    ```

## 独立部署时项目路径

```text
# 路径, 域名映射
main      /             leiax00.cn
novel     /             novel.leiax00.cn
tools     /             tools.leiax00.cn
```
部署方式按目前项目部署即可

## 合并部署时产物结构

```text
root                                  -- 主应用直接复制
 |-assets
 |-index.html
 |-novel                              -- novel子应用
 | |-assets
 | |-index.html
 | |-vite.svg
 |-tools                              -- tools子应用
 | |-assets
 | |-index.html
 | |-vite.svg
 |-vite.svg

```

子应用中 `base:/xxx` 来用以区分于主应用资源

### caddy配置

```text
:80 {
	@ui {
		not path /api/* # 定义ui文件匹配器
	}

	handle {
		root @ui /dist
		encode gzip
		try_files {path} index.html
		file_server
		header Access-Control-Allow-Origin *
		header Access-Control-Allow-Headers *
		header Access-Control-Allow-Methods *
	}
  
  handle /novel {
		root @ui /dist/novel
		encode gzip
		try_files {path} index.html
		file_server
		header Access-Control-Allow-Origin *
		header Access-Control-Allow-Headers *
		header Access-Control-Allow-Methods *
	}
  
  handle /tools {
		root @ui /dist/tools
		encode gzip
		try_files {path} index.html
		file_server
		header Access-Control-Allow-Origin *
		header Access-Control-Allow-Headers *
		header Access-Control-Allow-Methods *
	}

	handle /api/* {
		reverse_proxy {
			to https://leiax00.cn  # 本地使用代理到https不可用
			header_down Access-Control-Allow-Origin *
			header_down Access-Control-Allow-Methods *
			header_down Access-Control-Allow-Headers *
		}
	}
}

```