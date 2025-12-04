# 代理源配置说明：
# name: 代理源名称
# url: 代理列表基础URL
# parser: 解析方法（对应crawler中的parse_*方法）
# pages: 爬取页数
# delay: 分页请求延迟（防反爬）

# 普通代理源
NORMAL_PROXIES = [

]

# 高匿代理源
ANONYMOUS_PROXIES = [
    {
        "name": "齐云代理(高匿)",
        "url": "https://www.qiyunip.com/freeProxy/",
        "parser": "html4",
        "pages": 6,
        "delay": 2
    },
]
