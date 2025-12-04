import threading
from typing import List

import requests


class ProxyValidator:
    """代理IP验证类：多线程验证代理有效性"""

    def __init__(self, timeout: int = 10):
        self.valid_proxies = []  # 存储有效代理
        self.timeout = timeout  # 代理验证超时时间
        # 验证请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

    def check_proxy(self, proxy: str, test_url: str, keyword: str, encoding: str = "utf-8"):
        """
        验证单个代理有效性
        :param proxy: 待验证代理（IP:PORT）
        :param test_url: 测试URL
        :param keyword: 验证成功关键词
        :param encoding: 页面编码
        """
        try:
            proxy_config = {"http": proxy, "https": proxy}
            response = requests.get(
                test_url,
                headers=self.headers,
                proxies=proxy_config,
                timeout=self.timeout,
                allow_redirects=False,  # 禁止重定向，提高验证准确性
                verify=False  # 忽略SSL证书错误
            )
            response.encoding = encoding
            if keyword in response.text:
                self.valid_proxies.append(proxy)
        except:
            # 验证失败（超时/连接错误/关键词不匹配）不做处理
            pass

    def validate(self, proxies: List[str], test_url: str, keyword: str, thread_count: int = 500) -> List[str]:
        """
        批量验证代理IP（多线程）
        :param proxies: 待验证代理列表
        :param test_url: 测试URL
        :param keyword: 验证成功关键词
        :param thread_count: 单次最大线程数
        :return: 有效代理列表
        """
        threads = []
        self.valid_proxies.clear()

        if not proxies:
            print("⚠️ 无待验证的代理IP")
            return []

        # 分批次启动线程（避免线程数过多）
        for batch_start in range(0, len(proxies), thread_count):
            batch_proxies = proxies[batch_start:batch_start + thread_count]
            for proxy in batch_proxies:
                t = threading.Thread(
                    target=self.check_proxy,
                    args=(proxy, test_url, keyword)
                )
                threads.append(t)
                t.start()

            # 等待当前批次线程完成
            for t in threads[batch_start:batch_start + thread_count]:
                t.join()

        print(f"✅ 验证完成 | 有效代理：{len(self.valid_proxies)}个（总待验证：{len(proxies)}个）")
        return self.valid_proxies
