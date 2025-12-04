# FreeProxyPool 免费代理IP池

一款轻量、高效的免费代理IP池工具，支持多线程爬取、自动验证、定时更新，整合10+优质免费代理源，快速构建可用代理池，输出标准JSON格式，无缝对接爬虫、测试等各类需求。

```
 _____   _____    _____   _____   _____   _____    _____  __    __ __    __  _____   _____   _____   _      
|  ___| |  _  \  | ____| | ____| |  _  \ |  _  \  /  _  \ \ \  / / \ \  / / |  _  \ /  _  \ /  _  \ | |     
| |__   | |_| |  | |__   | |__   | |_| | | |_| |  | | | |  \ \/ /   \ \/ /  | |_| | | | | | | | | | | |     
|  __|  |  _  /  |  __|  |  __|  |  ___/ |  _  /  | | | |   }  {     \  /   |  ___/ | | | | | | | | | |     
| |     | | \ \  | |___  | |___  | |     | | \ \  | |_| |  / /\ \    / /    | |     | |_| | | |_| | | |___  
|_|     |_|  \_\ |_____| |_____| |_|     |_|  \_\ \_____/ /_/  \_\  /_/     |_|     \_____/ \_____/ |_____| 
```

## 核心特性

✅ **多源聚合**：整合10+主流免费代理源，覆盖高匿、普通代理类型  
✅ **自动验证**：多线程验证代理有效性，过滤无效、超时节点  
✅ **定时更新**：支持自定义循环间隔，持续维护可用代理池  
✅ **轻量高效**：无复杂依赖，配置简单，运行占用资源少  
✅ **标准输出**：JSON格式存储结果，方便对接爬虫、接口测试等场景  
✅ **易于扩展**：模块化设计，新增代理源仅需添加对应解析规则

## 已支持的免费代理源

| 代理名称          | 状态 | 代理类型  | 官方地址                            |
|:--------------|:--:|-------|:--------------------------------|
| 云代理           | ✅  | 普通/高匿 | <http://www.ip3366.net>         |
| 快代理           | ✅  | 普通/高匿 | <https://www.kuaidaili.com>     |
| 站大爷           | ❌  | 高匿    | <https://www.zdaye.com/>        |
| 开心代理          | ✅  | 普通/高匿 | <http://www.kxdaili.com>        |
| 积流代理          | ✅  | 高匿    | <https://www.jiliuip.com>       |
| 齐云代理          | ✅  | 高匿    | <https://www.qiyunip.com>       |
| 89免费代理        | ✅  | 未知    | <https://www.89ip.cn/>          |
| 小幻HTTP代理      | ❌  | 高匿    | <https://ip.ihuan.me>           |
| 911Proxy      | ✅  | 普通/高匿 | <https://www.911proxy.com>      |
| FineProxy     | ✅  | 普通/高匿 | <https://fineproxy.org>         |
| LumiProxy     | ✅  | 普通/高匿 | <https://www.lumiproxy.com>     |
| ProxyLite     | ✅  | 普通/高匿 | <https://www.proxylite.com>     |
| ProxyShare    | ✅  | 普通/高匿 | <https://www.proxyshare.com>    |
| ProxyScrape   | ✅  | 普通/高匿 | <https://api.proxyscrape.com>   |
| Proxy-Tools   | ❌  | 普通/高匿 | <https://proxy-tools.com>       |
| OpenProxyList | ✅  | 高匿    | <https://api.openproxylist.xyz> |

> 注：免费代理源稳定性受第三方影响，若部分源失效可在Issues反馈；欢迎推荐优质新代理源！

## 快速使用

### 1. 环境准备

- Python 3.8+
- 依赖安装：
  ```bash
  pip install -r requirements.txt
  ```

### 2. 运行程序

```bash
python main.py
```

### 3. 交互配置

运行后根据提示完成简单配置：

```
📌 代理IP爬取验证程序 - 配置向导
============================================================
请输入代理循环检查间隔时间（小时，默认2h）：
请选择爬取的代理类型（all-全部/normal-普通/anonymous-高匿，默认all）：
```

- 循环间隔：默认2小时，支持自定义（如输入`1`表示1小时更新一次）
- 代理类型：支持`all`（全部）、`normal`（普通代理）、`anonymous`（高匿代理）

### 4. 结果输出

- 有效代理将保存至 `proxy_ip.json` 文件，格式如下：
  ```json
  {
    "normal_proxies": ["123.45.67.89:8080", ...],  // 普通代理
    "anonymous_proxies": ["98.76.54.32:3128", ...], // 高匿代理
    "update_time": "2025-12-05 10:30:25"           // 最后更新时间
  }
  ```
- 运行日志实时显示爬取进度、验证结果、有效率等信息

## 运行截图

![运行截图](https://raw.githubusercontent.com/Fog-Forest/free-proxy-pool/main/images/screenshot.png)

## 扩展指南（新增代理源）

1. 在 `config/proxy_sources.py` 中添加代理源配置（参考现有格式）：
   ```python
   # 示例：新增XX代理
   NEW_PROXY = {
       "name": "XX代理",
       "url": "https://www.xxx.com/free/{page}/",  # 分页URL模板
       "parser": "parse_html2",  # 选择对应解析器（如parse_html1/parse_api1等）
       "pages": 5,  # 爬取页数，支持"auto"自动识别
       "delay": 1  # 爬取间隔（秒），避免请求过快
   }
   ```
2. 若需自定义解析规则，在 `utils/crawler.py` 中新增解析方法（如`parse_xxx`），参考现有解析器逻辑

## 注意事项

1. 本工具仅用于学习和测试，请勿用于非法用途，遵守目标网站 robots.txt 协议
2. 免费代理IP稳定性和安全性较差，建议仅用于非敏感场景；生产环境推荐使用商业代理服务
3. 部分代理源可能存在访问频率限制，可通过调整 `delay` 参数（爬取间隔）避免被封禁
4. 若运行中出现报错，大概率是代理源页面结构变更，可反馈至Issues或自行适配解析规则

## 贡献说明

- 发现Bug或代理源失效，欢迎提交 [Issues](https://github.com/Fog-Forest/free-proxy-pool/issues)
- 推荐优质免费代理源、新增解析规则，欢迎提交 [Pull Request](https://github.com/Fog-Forest/free-proxy-pool/pulls)
- 有功能需求或优化建议，可在Issues中讨论

## 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](https://github.com/Fog-Forest/free-proxy-pool/blob/main/LICENSE) 文件