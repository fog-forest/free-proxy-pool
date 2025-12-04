# FreeProxyPool - Free Proxy IP Pool

A lightweight and efficient free proxy IP pool tool that supports multi-threaded crawling, automatic validation,
scheduled updates, and integrates 10+ high-quality free proxy sources. Quickly build an available proxy pool with
standard JSON output, seamlessly integrating with crawlers, testing, and other use cases.

```
 _____   _____    _____   _____   _____   _____    _____  __    __ __    __  _____   _____   _____   _      
|  ___| |  _  \  | ____| | ____| |  _  \ |  _  \  /  _  \ \ \  / / \ \  / / |  _  \ /  _  \ /  _  \ | |     
| |__   | |_| |  | |__   | |__   | |_| | | |_| |  | | | |  \ \/ /   \ \/ /  | |_| | | | | | | | | | | |     
|  __|  |  _  /  |  __|  |  __|  |  ___/ |  _  /  | | | |   }  {     \  /   |  ___/ | | | | | | | | | |     
| |     | | \ \  | |___  | |___  | |     | | \ \  | |_| |  / /\ \    / /    | |     | |_| | | |_| | | |___  
|_|     |_|  \_\ |_____| |_____| |_|     |_|  \_\ \_____/ /_/  \_\  /_/     |_|     \_____/ \_____/ |_____| 
```

## Core Features

✅ **Multi-source Aggregation**: Integrates 10+ mainstream free proxy sources, covering elite and regular proxy types  
✅ **Automatic Validation**: Multi-threaded proxy validity check to filter invalid and timeout nodes  
✅ **Scheduled Updates**: Supports custom cycle intervals for continuous maintenance of the available proxy pool  
✅ **Lightweight & Efficient**: No complex dependencies, simple configuration, and low resource consumption  
✅ **Standard Output**: Stores results in JSON format for easy integration with crawlers, API testing, etc.  
✅ **Easy to Extend**: Modular design, adding new proxy sources only requires corresponding parsing rules

## Supported Free Proxy Sources

| Proxy Name    | Status | Proxy Type    | Official Website                |
|:--------------|:------:|:--------------|:--------------------------------|
| 云代理           |   ✅    | Regular/Elite | <http://www.ip3366.net>         |
| 快代理           |   ✅    | Regular/Elite | <https://www.kuaidaili.com>     |
| 站大爷           |   ❌    | Elite         | <https://www.zdaye.com>         |
| 开心代理          |   ✅    | Regular/Elite | <http://www.kxdaili.com>        |
| 积流代理          |   ✅    | Elite         | <https://www.jiliuip.com>       |
| 齐云代理          |   ✅    | Elite         | <https://www.qiyunip.com>       |
| 89免费代理        |   ✅    | Unknown       | <https://www.89ip.cn>           |
| 小幻HTTP代理      |   ❌    | Elite         | <https://ip.ihuan.me>           |
| 911Proxy      |   ✅    | Regular/Elite | <https://www.911proxy.com>      |
| FineProxy     |   ✅    | Regular/Elite | <https://fineproxy.org>         |
| LumiProxy     |   ✅    | Regular/Elite | <https://www.lumiproxy.com>     |
| ProxyLite     |   ✅    | Regular/Elite | <https://www.proxylite.com>     |
| ProxyShare    |   ✅    | Regular/Elite | <https://www.proxyshare.com>    |
| ProxyScrape   |   ✅    | Regular/Elite | <https://api.proxyscrape.com>   |
| Proxy-Tools   |   ❌    | Regular/Elite | <https://proxy-tools.com>       |
| OpenProxyList |   ✅    | Elite         | <https://api.openproxylist.xyz> |

> Note: The stability of free proxy sources is subject to third-party availability. Please report any inactive sources
> via Issues. Recommendations for high-quality new proxy sources are welcome!

## Quick Start

### 1. Environment Preparation

- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### 2. Run the Program

```bash
python main.py
```

### 3. Interactive Configuration

Complete the simple configuration as prompted after running:

```
📌 Proxy IP Crawling & Validation Program - Configuration Wizard
============================================================
Please enter the proxy cycle check interval (hours, default: 2h):
Please select the proxy type to crawl (all/normal/anonymous, default: all):
```

- Cycle Interval: Default is 2 hours, supports custom values (e.g., enter `1` for 1-hour updates)
- Proxy Type: Supports `all` (all types), `normal` (regular proxies), `anonymous` (elite proxies)

### 4. Result Output

- Valid proxies will be saved to `proxy_ip.json` with the following format:
  ```json
  {
    "summary": {
      "normal_count": 0,
      "anonymous_count": 6,
      "total_count": 6,
      "update_time": "2025-12-05 10:30:25"
    },
    "proxy_list": {
      "normal": ["123.45.67.89:8080", ...],  // Regular proxies
      "anonymous": ["98.76.54.32:3128", ...] // Elite proxies
    }
  }
  ```
- Runtime logs display real-time crawling progress, validation results, availability rate, and other information

## Screenshot

![Screenshot](https://raw.githubusercontent.com/Fog-Forest/free-proxy-pool/main/images/screenshot.png)

## Extension Guide (Add New Proxy Sources)

1. Add proxy source configuration in `config/proxy_sources.py` (refer to existing formats):
   ```python
   # Example: Add XX Proxy
   NEW_PROXY = {
       "name": "XX Proxy",
       "url": "https://www.xxx.com/free/{page}/",  # Pagination URL template
       "parser": "parse_html2",  # Corresponding parser method (e.g., parse_html1/parse_api1)
       "pages": 5,  # Number of pages to crawl, supports "auto" for automatic detection
       "delay": 1  # Pagination request delay (seconds) to avoid anti-crawling
   }
   ```
2. For custom parsing rules, add a new parsing method (e.g., `parse_xxx`) in `utils/crawler.py` by referring to existing
   parser logic

## Notes

1. This tool is for learning and testing purposes only. Do not use it for illegal activities. Comply with the
   `robots.txt` protocol of target websites.
2. Free proxy IPs have poor stability and security. It is recommended for non-sensitive scenarios only. Commercial proxy
   services are recommended for production environments.
3. Some proxy sources may have access frequency limits. Adjust the `delay` parameter (crawling interval) to avoid being
   blocked.
4. If errors occur during operation, it is likely due to changes in the proxy source's page structure. Please report to
   Issues or adapt the parsing rules yourself.

## Contribution Guidelines

- Found a bug or inactive proxy source? Submit an [Issue](https://github.com/Fog-Forest/free-proxy-pool/issues)
- Recommend high-quality free proxy sources or add new parsing rules? Submit
  a [Pull Request](https://github.com/Fog-Forest/free-proxy-pool/pulls)
- Have feature requests or optimization suggestions? Discuss in Issues

## License

This project is open-source under the MIT License. See
the [LICENSE](https://github.com/Fog-Forest/free-proxy-pool/blob/main/LICENSE) file for details.