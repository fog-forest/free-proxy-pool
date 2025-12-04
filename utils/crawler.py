import json
import re
import time
from typing import List

import requests
from bs4 import BeautifulSoup


class ProxyCrawler:
    """代理IP爬虫类"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        self.proxies = []  # 存储爬取的代理IP

    def fetch(self, url: str, timeout: int = 5) -> str:
        """请求页面，返回源码"""
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            return response.text
        except Exception as e:
            print(f"❌ 请求失败 {url}：{str(e)[:50]}")
            return ""

    @staticmethod
    def parse_api1(html: str) -> List[str]:
        """解析API响应，提取IP:PORT格式"""
        return re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', html)

    @staticmethod
    def parse_api2(html: str) -> List[str]:
        """解析JSON接口，提取protocol=1/2的IP+Port"""
        result = []
        try:
            data = json.loads(html)

            # 兼容不同JSON结构提取代理列表
            proxy_list = []
            if isinstance(data.get("data"), dict):
                proxy_list = data["data"].get("list", [])
            elif isinstance(data, list):
                proxy_list = data
            elif isinstance(data.get("list"), list):
                proxy_list = data["list"]

            if not proxy_list:
                print("⚠️ JSON接口无代理数据")
                return result

            # 过滤有效代理
            valid_protocol = {1, 2}
            total = len(proxy_list)
            filtered = 0

            for proxy in proxy_list:
                protocol = proxy.get("protocol")
                ip = proxy.get("ip")
                port = proxy.get("port")

                # 校验IP/端口/协议合法性
                ip_valid = isinstance(ip, str) and re.match(r'\d+\.\d+\.\d+\.\d+', ip)
                port_valid = isinstance(port, (int, str)) and str(port).isdigit()
                protocol_valid = protocol in valid_protocol

                if ip_valid and port_valid and protocol_valid:
                    result.append(f"{ip}:{str(port).strip()}")
                    print(f"{ip}:{str(port).strip()}")
                    filtered += 1

            print(f"✅ JSON解析完成 | 总数：{total} | 有效：{filtered}")
            return result

        except json.JSONDecodeError:
            print("❌ 非有效JSON格式")
            return result
        except Exception as e:
            print(f"❌ JSON解析异常：{str(e)[:50]}")
            return result

    @staticmethod
    def parse_article1(html: str) -> List[str]:
        """解析文章页面，提取IP:PORT格式"""
        return re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', html)

    @staticmethod
    def parse_html1(html: str) -> List[str]:
        """解析HTML，IP+端口在同一个td标签"""
        soup = BeautifulSoup(html, 'html5lib')
        trs = soup.find_all('tr')
        return [tr.find_all('td')[0].text.strip() for tr in trs[1:]]

    @staticmethod
    def parse_html2(html: str) -> List[str]:
        """解析HTML，IP在第1个td，端口在第2个td"""
        soup = BeautifulSoup(html, 'html5lib')
        trs = soup.find_all('tr')
        return [f"{tr.find_all('td')[0].text.strip()}:{tr.find_all('td')[1].text.strip()}"
                for tr in trs[1:]]

    @staticmethod
    def parse_html3(html: str) -> List[str]:
        """解析HTML，IP在第2个td，端口在第3个td"""
        soup = BeautifulSoup(html, 'html5lib')
        trs = soup.find_all('tr')
        return [f"{tr.find_all('td')[1].text.strip()}:{tr.find_all('td')[2].text.strip()}"
                for tr in trs[1:]]

    @staticmethod
    def parse_html4(html: str) -> List[str]:
        """解析HTML，IP在第1个th，端口在第2个th"""
        soup = BeautifulSoup(html, 'html5lib')
        trs = soup.find_all('tr')
        return [f"{tr.find_all('th')[0].text.strip()}:{tr.find_all('th')[1].text.strip()}"
                for tr in trs[1:]]

    @staticmethod
    def parse_fpslist(html: str) -> List[str]:
        """解析fpsList格式JSON，提取ip+port"""
        pattern = r'const fpsList = (\[.*?\]);'
        match = re.search(pattern, html, re.DOTALL)
        if not match:
            print("⚠️ 未找到fpsList数据")
            return []
        try:
            proxy_list = json.loads(match.group(1))
            result = []
            for item in proxy_list:
                if "ip" in item and "port" in item:
                    result.append(f"{item['ip']}:{item['port']}")
            return result
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败：{str(e)[:50]}")
            return []

    def _get_auto_page_count(self, url: str) -> int:
        """内部方法：自动获取api2总页数"""
        first_page_url = url + "1" if url.endswith("page=") else url
        html = self.fetch(first_page_url)
        if not html:
            print("❌ 自动获取总页数失败")
            return 1
        try:
            data = json.loads(html)
            page_count = 0
            if isinstance(data.get("data"), dict):
                page_count = data["data"].get("page_count",
                                              data["data"].get("total_pages",
                                                               data["data"].get("total_page", 0)))
            page_count = page_count or data.get("page_count", 0)
            return page_count if page_count > 0 else 1
        except Exception:
            print("❌ 解析总页数失败")
            return 1

    def crawl(self, source: dict) -> int:
        """爬取指定源代理IP"""
        parser = getattr(self, f"parse_{source['parser']}", None)
        if not parser:
            print(f"❌ 未知解析器：{source['parser']}")
            return 0

        crawl_count = 0
        try:
            # 处理pages：支持 "auto" / 函数 / 固定数值
            if source['pages'] == "auto":
                # 自动获取总页数，仅api2支持
                if source['parser'] != "api2":
                    print("⚠️ 仅api2支持pages='auto'")
                    total_pages = 1
                else:
                    total_pages = self._get_auto_page_count(source['url'])
                    print(f"🔍 自动获取总页数：{total_pages}")
            elif callable(source['pages']):
                # 支持函数获取总页数
                total_pages = source['pages'](source['url'])
                print(f"🔍 函数获取总页数：{total_pages}")
            else:
                # 固定数值总页数
                total_pages = source['pages']

            # 分页爬取
            for current_page in range(1, total_pages + 1):
                if source['parser'] == "api2":
                    if "page=" in source['url']:
                        if source['url'].endswith("page="):
                            url = source['url'] + str(current_page)
                        else:
                            url = re.sub(r'page=\d+', f'page={current_page}', source['url'])
                    else:
                        url = f"{source['url']}&page={current_page}"
                elif "api1" in source['parser']:
                    url = source['url']
                elif "kxdaili.com" in source['url'] or "qiyunip.com" in source['url']:
                    url = f"{source['url']}{current_page}.html"
                else:
                    url = f"{source['url']}{current_page}"

                print(f"\n🔍 正在爬取 {source['name']} | 页码：{current_page}/{total_pages} | URL：{url}")
                html = self.fetch(url)

                if current_page == 1:
                    print(f"📄 响应预览：{html[:500]}...")
                if not html:
                    print(f"⚠️ 第{current_page}页为空，跳过")
                    time.sleep(source['delay'])
                    continue

                ips = parser(html)
                print(f"✅ 第{current_page}页提取到 {len(ips)} 个IP")
                self.proxies.extend(ips)
                crawl_count += len(ips)

                time.sleep(source['delay'])

        except Exception as e:
            print(f"❌ 爬取失败 {source['name']}：{str(e)[:50]}")

        print(f"\n🔍 {source['name']} 爬取完成 | 总计：{crawl_count} 个IP")
        return crawl_count

    def get_unique_proxies(self) -> List[str]:
        """代理IP去重"""
        unique_list = list(set(self.proxies))
        self.proxies.clear()
        return unique_list
