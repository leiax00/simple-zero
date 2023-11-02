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
## 项目路径
```text
# 路径, 域名映射
main      /             leiax00.cn
novel     /novel        leiax00.cn/novel
tools     /tools        leiax00.cn/tools
```
各个微应用可以单独部署, 最终在代理上按上述域名路径进行代理即可, 路径透传无截取
