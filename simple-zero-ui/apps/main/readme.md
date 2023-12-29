# UI MAIN
[服务应用详细说明文档](https://www.notion.so/leiax00/UI-MAIN-ef2a97858951424b8692f2d06ac52d53)

## 配置文件

```json
{
	"app": {
		"title": "Simple-Zero",
		"version": "v0.0.1",
		"baseUrl": "",
		"firstRun": "2021-11-15T17:00:00",
		"copyright": "xxxxx",
		"picCdn": {
			"base": "xxxxxxxxx",
			"opts": {
				"pic": "pics"
			}
		},
		"srcSvg": "//at.alicdn.com/t/c/font_2015893_n3j0e7lbb.js",
		"notionToken": "xxxxxxxxx"
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
		"domain": "xxxxxxxx"
	}]
}
```