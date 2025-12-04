import time

from config.proxy_sources import NORMAL_PROXIES, ANONYMOUS_PROXIES
from utils.crawler import ProxyCrawler
from utils.storage import ProxyStorage
from utils.validator import ProxyValidator


def main():
    # 输入交互
    print("=" * 60)
    print("📌 代理IP爬取验证程序 - 配置向导")
    print("=" * 60)
    check_hours = input("请输入代理循环检查间隔时间（小时，默认2h）：").strip()
    check_hours = int(check_hours) if check_hours and check_hours.isdigit() else 2
    check_interval = check_hours * 3600

    # 代理类型选择
    proxy_type = input("请选择爬取的代理类型（all-全部/normal-普通/anonymous-高匿，默认all）：").strip().lower() or "all"
    while proxy_type not in ["all", "normal", "anonymous"]:
        print("❌ 错误：仅支持 all/normal/anonymous 三种输入！")
        proxy_type = input("请重新输入代理类型：").strip().lower() or "all"

    thread_count = 1000  # 线程数可适当调整
    test_config = {
        "url": "http://captive.apple.com/",
        "keyword": "Success",
        "encoding": "utf-8"
    }

    # 启动信息
    print("\n" + "=" * 80)
    print("🚀 代理IP爬取验证程序 启动成功")
    print("=" * 80)
    print(f"📋 核心配置：")
    print(f"   ├─ 爬取类型：{proxy_type}（all=全部 / normal=普通 / anonymous=高匿）")
    print(f"   ├─ 检查间隔：{check_hours} 小时（{check_interval} 秒）")
    print(f"   ├─ 验证线程数：{thread_count} 个")
    print(f"   └─ 测试URL：{test_config['url']}")
    print("=" * 80 + "\n")

    while True:
        # 初始化爬虫实例
        crawler_normal = ProxyCrawler() if proxy_type in ["all", "normal"] else None
        crawler_anonymous = ProxyCrawler() if proxy_type in ["all", "anonymous"] else None

        # 爬取普通代理
        normal_proxies = []
        if proxy_type in ["all", "normal"]:
            print("📥 [阶段1/3] 开始爬取 普通代理 IP...")
            print("-" * 50)
            for source in NORMAL_PROXIES:
                crawler_normal.crawl(source)
            print("\n🔍 [普通代理] 开始去重...")
            normal_proxies = crawler_normal.get_unique_proxies()
            print(f"✅ [普通代理] 最终可用IP数：{len(normal_proxies)} 个\n")

        # 爬取高匿代理
        anonymous_proxies = []
        if proxy_type in ["all", "anonymous"]:
            print("📥 [阶段1/3] 开始爬取 高匿代理 IP...")
            print("-" * 50)
            for source in ANONYMOUS_PROXIES:
                crawler_anonymous.crawl(source)
            print("\n🔍 [高匿代理] 开始去重...")
            anonymous_proxies = crawler_anonymous.get_unique_proxies()
            print(f"✅ [高匿代理] 最终可用IP数：{len(anonymous_proxies)} 个\n")

        # 合并代理并统计
        proxy_with_type = []
        for ip in normal_proxies:
            proxy_with_type.append((ip, "normal"))
        for ip in anonymous_proxies:
            proxy_with_type.append((ip, "anonymous"))
        all_proxies = [item[0] for item in proxy_with_type]

        # 爬取结果汇总
        print("=" * 60)
        print("📊 爬取结果汇总")
        print("=" * 60)
        print(f"   ├─ 普通代理：{len(normal_proxies):3d} 个")
        print(f"   ├─ 高匿代理：{len(anonymous_proxies):3d} 个")
        print(f"   └─ 总待验证：{len(all_proxies):3d} 个")
        print("=" * 60 + "\n")

        # 批量验证
        valid_normal, valid_anonymous = [], []
        if all_proxies:
            print("🔍 [阶段2/3] 开始批量验证代理有效性...")
            print(f"ℹ️  验证配置：线程数={thread_count} | 测试URL={test_config['url']}")
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

            # 去重冲突（优先保留高匿）
            valid_normal = [ip for ip in valid_normal if ip not in valid_anonymous]

            # 验证结果显示
            print(f"\n✅ [验证完成]")
            print(f"   ├─ 总待验证：{len(all_proxies):3d} 个")
            print(f"   ├─ 有效代理：{len(valid_proxies):3d} 个")
            print(f"   ├─ 有效率：{(len(valid_proxies) / len(all_proxies) * 100):6.2f}%")
            print(f"   ├─ 有效普通代理：{len(valid_normal):3d} 个（示例：{valid_normal[:2]}）")
            print(f"   └─ 有效高匿代理：{len(valid_anonymous):3d} 个（示例：{valid_anonymous[:2]}）")
        else:
            print("⚠️ [阶段2/3] 无待验证的代理IP，跳过验证步骤")

        # 保存结果
        print("\n" + "=" * 60)
        print("💾 [阶段3/3] 保存有效代理IP...")
        ProxyStorage.save_proxies_with_type(
            filename="proxy_ip.json",
            normal_proxies=valid_normal,
            anonymous_proxies=valid_anonymous
        )

        # 保存结果汇总
        total_valid = len(valid_normal) + len(valid_anonymous)
        print(f"✅ 保存完成！")
        print(f"   ├─ 保存文件：proxy_ip.json")
        print(f"   ├─ 有效普通代理：{len(valid_normal):3d} 个")
        print(f"   ├─ 有效高匿代理：{len(valid_anonymous):3d} 个")
        print(f"   └─ 总计有效代理：{total_valid:3d} 个")
        print("=" * 60)

        # 下一轮提示
        next_round = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + check_interval))
        print(f"\n⏰ 本轮任务完成！{check_hours}小时后（预计 {next_round}）开始下一轮检查")
        print("-" * 80 + "\n")
        time.sleep(check_interval)


if __name__ == "__main__":
    main()
