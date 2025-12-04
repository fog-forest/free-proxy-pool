# 代理源配置说明：
# name: 代理源名称（区分类型和特性）
# url: 代理列表基础URL（分页参数留空或占位）
# body: POST请求数据（可选，为空则使用GET请求）
# parser: 解析方法（对应crawler中的parse_*方法）
# pages: 爬取页数（固定数值/auto自动识别，api2方法专属）
# delay: 分页请求延迟（秒，防反爬）

# 普通代理源（透明代理/普通匿名代理）
NORMAL_PROXIES = [
    {
        "name": "云代理(普通)",
        "url": "http://www.ip3366.net/free/?stype=2&page=",
        "parser": "html2",
        "pages": 2,
        "delay": 2,
    },
    {
        "name": "开心代理(普通)",
        "url": "http://www.kxdaili.com/dailiip/2/",
        "parser": "html2",
        "pages": 10,
        "delay": 5,
    },
    {
        "name": "快代理国内(普通)",
        "url": "https://www.kuaidaili.com/free/intr/",
        "parser": "fpslist",
        "pages": 6,
        "delay": 2,
    },
    {
        "name": "89免费代理(未知)",
        "url": "http://api.89ip.cn/tqdl.html?api=1&num=3000&port=&address=&isp=",
        "parser": "api1",
        "pages": 1,
        "delay": 1,
    },
    {
        "name": "911Proxy(透明)",
        "url": "https://www.911proxy.com/web_v1/free-proxy/list?anonymity=0&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "911Proxy(普通)",
        "url": "https://www.911proxy.com/web_v1/free-proxy/list?anonymity=1&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "FineProxy(普通)",
        "url": "https://fineproxy.org/wp-admin/admin-ajax.php",
        "body": {
            "action": "proxylister_load_more",
            "nonce": "915fbd1f83",
            "page": "{page}",  # 分页占位符，会自动替换为当前页码
            "atts[protocols]": "HTTP,HTTPS",
            "atts[anonymity]": "Anonymous,Transparent",
            "atts[latency]": "0",
            "atts[uptime]": "0",
            "atts[last_checked]": "180",
            "atts[trp-form-language]": "cn",
            "atts[page_size]": "20"
        },
        "parser": "fineproxy",
        "pages": 10,
        "delay": 3,
    },
    {
        "name": "LumiProxy(透明)",
        "url": "https://api.lumiproxy.com/web_v1/free-proxy/list?anonymity=0&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "LumiProxy(普通)",
        "url": "https://api.lumiproxy.com/web_v1/free-proxy/list?anonymity=1&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "ProxyLite(透明)",
        "url": "https://www.proxylite.com/web_v1/free-proxy/list?anonymity=0&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "ProxyLite(普通)",
        "url": "https://www.proxylite.com/web_v1/free-proxy/list?anonymity=1&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "ProxyShare(透明)",
        "url": "https://www.proxyshare.com/web_v1/free-proxy/list?anonymity=0&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "ProxyShare(普通)",
        "url": "https://www.proxyshare.com/web_v1/free-proxy/list?anonymity=1&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "ProxyScrape(普通)",
        "url": "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=protocolipport&format=text&anonymity=Anonymous,Transparent&timeout=20000",
        "parser": "api1",
        "pages": 1,
        "delay": 1,
    }
]

# 高匿代理源（高匿名代理）
ANONYMOUS_PROXIES = [
    {
        "name": "云代理(高匿)",
        "url": "http://www.ip3366.net/free/?stype=1&page=",
        "parser": "html2",
        "pages": 2,
        "delay": 2,
    },
    {
        "name": "开心代理(高匿)",
        "url": "http://www.kxdaili.com/dailiip/1/",
        "parser": "html2",
        "pages": 10,
        "delay": 5,
    },
    {
        "name": "积流代理(高匿)",
        "url": "https://www.jiliuip.com/free/page-",
        "parser": "fpslist",
        "pages": 10,
        "delay": 2,
    },
    {
        "name": "齐云代理(高匿)",
        "url": "https://www.qiyunip.com/freeProxy/",
        "parser": "html4",
        "pages": 6,
        "delay": 2,
    },
    {
        "name": "快代理优质(高匿)",
        "url": "https://www.kuaidaili.com/free/dps/",
        "parser": "fpslist",
        "pages": 4,
        "delay": 2,
    },
    {
        "name": "快代理国内(高匿)",
        "url": "https://www.kuaidaili.com/free/inha/",
        "parser": "fpslist",
        "pages": 6,
        "delay": 2,
    },
    {
        "name": "快代理海外(高匿)",
        "url": "https://www.kuaidaili.com/free/fps/",
        "parser": "fpslist",
        "pages": 25,
        "delay": 2,
    },
    {
        "name": "911Proxy(高匿)",
        "url": "https://www.911proxy.com/web_v1/free-proxy/list?anonymity=2&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "FineProxy(高匿)",
        "url": "https://fineproxy.org/wp-admin/admin-ajax.php",
        "body": {
            "action": "proxylister_load_more",
            "nonce": "915fbd1f83",
            "page": "{page}",  # 分页占位符
            "atts[protocols]": "HTTP,HTTPS",
            "atts[anonymity]": "Elite",
            "atts[latency]": "0",
            "atts[uptime]": "0",
            "atts[last_checked]": "180",
            "atts[trp-form-language]": "cn",
            "atts[page_size]": "20"
        },
        "parser": "fineproxy",
        "pages": 10,
        "delay": 3,
    },
    {
        "name": "LumiProxy(高匿)",
        "url": "https://api.lumiproxy.com/web_v1/free-proxy/list?anonymity=2&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "ProxyShare(高匿)",
        "url": "https://www.proxyshare.com/web_v1/free-proxy/list?anonymity=2&page_size=60&page=",
        "parser": "api2",
        "pages": "auto",
        "delay": 2,
    },
    {
        "name": "ProxyScrape(高匿)",
        "url": "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=protocolipport&format=text&anonymity=Elite&timeout=20000",
        "parser": "api1",
        "pages": 1,
        "delay": 1,
    },
    {
        "name": "OpenProxyList(高匿)",
        "url": "https://api.openproxylist.xyz/http.txt",
        "parser": "api1",
        "pages": 1,
        "delay": 1,
    },
    {
        "name": "OpenProxyList(高匿)",
        "url": "https://api.openproxylist.xyz/https.txt",
        "parser": "api1",
        "pages": 1,
        "delay": 1,
    }
]
