import json
import re
import time
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup


class ProxyCrawler:
    """代理IP爬虫类"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        self.proxies = []  # 存储爬取的代理IP

    def fetch(self, url: str, timeout: int = 5, post_data: Optional[Dict] = None) -> str:
        """请求页面，返回源码（支持GET/POST）"""
        try:
            if post_data:
                response = requests.post(url, headers=self.headers, data=post_data, timeout=timeout)
            else:
                response = requests.get(url, headers=self.headers, timeout=timeout)
            return response.text
        except Exception as e:
            print(f"❌ [请求失败] {url}：{str(e)[:50]}")
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
            proxy_list = []
            # 兼容多种JSON数据结构：data.data.list、data.list、直接是列表
            if isinstance(data.get("data"), dict):
                proxy_list = data["data"].get("list", [])
            elif isinstance(data, list):
                proxy_list = data
            elif isinstance(data.get("list"), list):
                proxy_list = data["list"]

            if not proxy_list:
                print("⚠️ [JSON接口] 无代理数据")
                return result

            valid_protocol = {1, 2}
            for proxy in proxy_list:
                protocol = proxy.get("protocol")
                ip = proxy.get("ip")
                port = proxy.get("port")
                protocol_valid = protocol in valid_protocol
                if protocol_valid and ip is not None and port is not None:
                    result.append(f"{str(ip).strip()}:{str(port).strip()}")

            return result
        except json.JSONDecodeError:
            print("❌ [JSON解析] 非有效JSON格式")
            return result
        except Exception as e:
            print(f"❌ [JSON解析] 异常：{str(e)[:50]}")
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
            print("⚠️ [fpsList解析] 未找到数据")
            return []

        try:
            proxy_list = json.loads(match.group(1))
            result = []
            for item in proxy_list:
                if "ip" in item and "port" in item:
                    result.append(f"{item['ip']}:{item['port']}")

            return result
        except json.JSONDecodeError as e:
            print(f"❌ [fpsList解析] JSON错误：{str(e)[:50]}")
            return []

    @staticmethod
    def parse_fineproxy(html: str) -> List[str]:
        """解析FineProxy的响应数据, 提取ip+port"""
        try:
            response_json = json.loads(html)
        except json.JSONDecodeError as e:
            print(f"❌ [FineProxy解析] JSON错误：{str(e)[:50]}")
            return []

        rows_html = response_json.get("data", {}).get("rows", "").strip()
        if not rows_html:
            print("⚠️ [FineProxy解析] 无有效数据（rows为空）")
            return []

        pattern = r'<td\s+class=["\']table-ip["\']\s*>\s*(\d+\.\d+\.\d+\.\d+)\s*</td>\s*<td\s*>\s*(\d+)\s*</td>'
        matches = re.findall(pattern, rows_html, re.IGNORECASE | re.DOTALL)
        if not matches:
            print("⚠️ [FineProxy解析] 未匹配到IP和端口")
            return []

        result = []
        for ip, port in matches:
            port_stripped = port.strip()
            if port_stripped:
                result.append(f"{ip}:{port_stripped}")

        return result

    def _get_auto_page_count(self, url: str) -> int:
        """内部方法：自动获取api2总页数"""
        first_page_url = url + "1" if url.endswith("page=") else url
        html = self.fetch(first_page_url)
        if not html:
            print("❌ [自动分页] 获取总页数失败")
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
            print("❌ [自动分页] 解析总页数失败")
            return 1

    def _is_valid_proxy(self, proxy: str) -> bool:
        """内部方法：校验代理IP:PORT的合法性"""
        if not proxy or ':' not in proxy:
            return False
        ip, port_str = proxy.split(':', 1)  # 分割IP和端口（仅分割一次，避免端口含:）

        # 1. IP合法性校验（IPv4：四段数字，每段0-255）
        ip_segments = ip.split('.')
        if len(ip_segments) != 4:
            return False
        try:
            ip_nums = [int(seg) for seg in ip_segments]
            if not all(0 <= num <= 255 for num in ip_nums):
                return False
        except ValueError:
            return False

        # 2. 端口合法性校验（1-65535，支持数字字符串）
        try:
            port = int(port_str.strip())
            if not (1 <= port <= 65535):
                return False
        except ValueError:
            return False

        return True

    def crawl(self, source: dict) -> int:
        """爬取指定源的代理IP"""
        parser = getattr(self, f"parse_{source['parser']}", None)
        if not parser:
            print(f"❌ [爬虫错误] 未知解析器：{source['parser']}")
            return 0

        # 分隔符
        source_name = source['name'].center(30, ' ')
        print(f"\n{'=' * 80}")
        print(f"📥 开始爬取 | {source_name}")
        print(f"{'=' * 80}")

        temp_proxies = []
        no_data_count = 0
        before_count = len(self.proxies)
        try:
            # 处理分页配置
            if source['pages'] == "auto":
                if source['parser'] != "api2":
                    print("⚠️ [分页警告] 仅api2支持自动分页，默认爬1页")
                    total_pages = 1
                else:
                    total_pages = self._get_auto_page_count(source['url'])
                    print(f"ℹ️ [分页信息] 自动获取总页数：{total_pages} 页")
            else:
                total_pages = source['pages']
                print(f"ℹ️ [分页信息] 配置爬取页数：{total_pages} 页")

            # 分页爬取
            for current_page in range(1, total_pages + 1):
                # 构建请求URL
                if "api1" in source['parser']:
                    url = source['url']
                elif source['parser'] in ["fineproxy"]:
                    url = source['url']
                elif any(domain in source['url'] for domain in ["kxdaili.com", "qiyunip.com"]):
                    url = f"{source['url']}{current_page}.html"
                else:
                    url = f"{source['url']}{current_page}"

                # 处理POST数据
                post_data = source.get("body") or None
                if post_data and isinstance(post_data, dict):
                    post_data = {k: v.replace("{page}", str(current_page)) if "{page}" in str(v) else v
                                 for k, v in post_data.items()}

                # 分页日志
                print(f"\n🔄 正在爬取 | 页码：{current_page:2d}/{total_pages:2d} | URL：{url}")
                print(f"ℹ️  当前累计 | 总列表IP数：{len(self.proxies):3d} 个")

                html = self.fetch(url, post_data=post_data)

                # 仅在第1页显示预览
                if current_page == 1 and html:
                    preview = html[:500].replace('\n', ' ').strip()  # 去除换行，精简显示
                    print(f"📄 响应预览：{preview}...")

                if not html:
                    print(f"⚠️  页码 {current_page:2d} | 请求失败，跳过")
                    no_data_count += 1
                else:
                    ips = parser(html)
                    valid_ips = [ip for ip in ips if self._is_valid_proxy(ip)]  # 校验结果
                    page_valid_count = len(valid_ips)

                    # 分页结果日志
                    print(f"✅  页码 {current_page:2d} | 提取IP：{len(ips):2d} 个 | 有效格式：{page_valid_count:2d} 个")

                    temp_proxies.extend(valid_ips)
                    no_data_count = 0 if page_valid_count > 0 else no_data_count + 1

                    if page_valid_count == 0:
                        print(f"⚠️  页码 {current_page:2d} | 无有效IP，连续无数据次数：{no_data_count}")

                # 连续3次无数据停止
                if no_data_count >= 3:
                    print(f"\n🛑 [爬取停止] 连续3次无有效IP，提前结束当前源爬取")
                    break

                time.sleep(source['delay'])

            # 爬取完成统计
            self.proxies.extend(temp_proxies)
            crawl_count = len(temp_proxies)
            after_count = len(self.proxies)
            print(f"\n{'=' * 80}")
            print(f"✅ 爬取完成 | {source['name']}")
            print(f"   ├─ 本源性新增有效IP：{crawl_count:3d} 个")
            print(f"   ├─ 总列表累计IP数：{after_count:3d} 个")
            print(f"   └─ 本次新增量：{after_count - before_count:3d} 个")
            print(f"{'=' * 80}")

        except Exception as e:
            print(f"\n{'=' * 80}")
            print(f"❌ 爬取失败 | {source['name']}")
            print(f"   ├─ 失败原因：{str(e)[:50]}")
            valid_temp = [ip for ip in temp_proxies if re.match(r'\d+\.\d+\.\d+\.\d+:\d+', ip)]
            crawl_count = len(valid_temp)
            if valid_temp:
                self.proxies.extend(valid_temp)
                after_count = len(self.proxies)
                print(f"   ├─ 异常恢复：已累计有效IP {crawl_count:3d} 个")
                print(f"   └─ 总列表当前累计：{after_count:3d} 个")
            print(f"{'=' * 80}")

        return crawl_count

    def get_unique_proxies(self) -> List[str]:
        """代理IP去重（优化日志显示）"""
        before_count = len(self.proxies)
        unique_list = list(set(self.proxies))
        after_count = len(unique_list)
        duplicate_count = before_count - after_count
        self.proxies.clear()

        # 计算重复率（处理除以0）
        duplicate_rate = (duplicate_count / before_count) * 100 if before_count != 0 else 0.0

        # 优化去重日志格式
        print(f"\n{'=' * 60}")
        print(f"🔍 代理IP去重统计")
        print(f"   ├─ 去重前总数量：{before_count:3d} 个")
        print(f"   ├─ 去重后总数量：{after_count:3d} 个")
        print(f"   ├─ 重复IP数量：{duplicate_count:3d} 个")
        print(f"   └─ 重复率：{duplicate_rate:6.2f}%")
        print(f"{'=' * 60}")

        return unique_list
