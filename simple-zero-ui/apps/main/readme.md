# UI MAIN

## 配置文件
```json
{
	"app": {
		"title": "Simple-Zero",
		"version": "v0.0.1",
		"baseUrl": "",
		"firstRun": "2021-11-15T17:00:00",
		"copyright": "蜀ICP备2020031548号-1",
		"picCdn": {
			"base": "https://webdav.leiax00.cn/dev",
			"opts": {
				"pic": "pics"
			}
		},
		"srcSvg": "//at.alicdn.com/t/c/font_2015893_n3j0e7lbb.js",
		"notionToken": "secret_QIkAfEfwEMDL6lByKGLFOf5EVylOMFf3KGeJPkix7z9"
	},
	"headers": [{
		"id": "index",
		"name": "首页",
		"path": "/index"
	}, {
		"id": "novel",
		"name": "小说",
		"path": "/novel"
	}],
	"serves": [{
		"name": "novel-ui",
		"prefix": "/novel",
		"domain": "https://novel.leiax00.cn"
	}]
}
```