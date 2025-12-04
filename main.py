import time

from config.proxy_sources import NORMAL_PROXIES, ANONYMOUS_PROXIES
from utils.crawler import ProxyCrawler
from utils.storage import ProxyStorage
from utils.validator import ProxyValidator


def main():
    # 基础配置
    check_interval = int(input("请输入代理循环检查间隔时间（秒，默认3600）：") or "3600")
    thread_count = 300  # 代理验证线程数

    # 新增：代理类型选择（支持全部/普通/高匿）
    proxy_type = input("请选择爬取的代理类型（all-全部/normal-普通/anonymous-高匿，默认all）：").strip().lower() or "all"
    # 校验输入合法性
    while proxy_type not in ["all", "normal", "anonymous"]:
        print("❌ 输入错误！仅支持 all/normal/anonymous")
        proxy_type = input("请重新选择代理类型（all/normal/anonymous）：").strip().lower() or "all"

    # 代理有效性测试配置
    test_config = {
        "url": "http://captive.apple.com/",  # 测试连通性的URL
        "keyword": "Success",  # 验证成功的关键词
        "encoding": "utf-8"  # 页面编码
    }

    print("\n===== 代理IP爬取验证程序启动 =====")
    print(f"爬取类型：{proxy_type}（all=全部/normal=普通/anonymous=高匿）")
    print(f"检查间隔：{check_interval}秒 | 验证线程数：{thread_count}")

    while True:
        # 1. 初始化爬虫实例（按需创建）
        crawler_normal = ProxyCrawler() if proxy_type in ["all", "normal"] else None
        crawler_anonymous = ProxyCrawler() if proxy_type in ["all", "anonymous"] else None

        # 爬取普通代理（按需执行）
        normal_proxies = []
        if proxy_type in ["all", "normal"]:
            print("\n【1/3】开始爬取普通代理IP...")
            for source in NORMAL_PROXIES:
                crawler_normal.crawl(source)
            normal_proxies = crawler_normal.get_unique_proxies()

        # 爬取高匿代理（按需执行）
        anonymous_proxies = []
        if proxy_type in ["all", "anonymous"]:
            print("\n【1/3】开始爬取高匿代理IP...")
            for source in ANONYMOUS_PROXIES:
                crawler_anonymous.crawl(source)
            anonymous_proxies = crawler_anonymous.get_unique_proxies()

        # 构建带类型标签的代理列表（格式：(ip, type)）
        proxy_with_type = []
        for ip in normal_proxies:
            proxy_with_type.append((ip, "normal"))
        for ip in anonymous_proxies:
            proxy_with_type.append((ip, "anonymous"))

        # 提取待验证的纯IP列表（用于批量验证）
        all_proxies = [item[0] for item in proxy_with_type]
        print(
            f"\n✅ 爬取完成 | 普通代理：{len(normal_proxies)}个 | 高匿代理：{len(anonymous_proxies)}个 | 总待验证：{len(all_proxies)}个")

        # 2. 批量验证所有代理（仅当有代理时执行）
        valid_normal, valid_anonymous = [], []
        if all_proxies:
            print("\n【2/3】开始批量验证所有代理有效性...")
            validator = ProxyValidator()
            valid_proxies = validator.validate(
                all_proxies,
                test_config["url"],
                test_config["keyword"],
                thread_count
            )

            # 按类型拆分有效代理
            valid_set = set(valid_proxies)
            for ip, type_tag in proxy_with_type:
                if ip in valid_set:
                    if type_tag == "normal":
                        valid_normal.append(ip)
                    else:
                        valid_anonymous.append(ip)

            # 可选：去重（同一个IP同时在普通/高匿中时，优先保留高匿）
            valid_normal = [ip for ip in valid_normal if ip not in valid_anonymous]
        else:
            print("\n⚠️ 无待验证的代理IP，跳过验证步骤")

        print(f"待保存普通代理：{len(valid_normal)}个，内容：{valid_normal[:3]}")
        print(f"待保存高匿代理：{len(valid_anonymous)}个，内容：{valid_anonymous[:3]}")

        # 3. 保存验证结果
        print("\n【3/3】保存有效代理IP...")
        ProxyStorage.save_proxies_with_type(
            filename="proxy_ip.json",
            normal_proxies=valid_normal,
            anonymous_proxies=valid_anonymous
        )

        # 等待下一轮检查
        print(f"\n===== 本轮完成，{check_interval}秒后开始下一轮检查 =====")
        time.sleep(check_interval)


if __name__ == "__main__":
    main()
