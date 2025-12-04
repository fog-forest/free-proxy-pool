import json
import time
from typing import List


class ProxyStorage:
    @staticmethod
    def save_proxies_with_type(filename: str, normal_proxies: List[str], anonymous_proxies: List[str]) -> None:
        """
        保存代理IP到JSON文件（区分普通/高匿类型）
        :param filename: 保存文件名
        :param normal_proxies: 有效普通代理列表
        :param anonymous_proxies: 有效高匿代理列表
        """
        save_data = {
            "summary": {
                "normal_count": len(normal_proxies),
                "anonymous_count": len(anonymous_proxies),
                "total_count": len(normal_proxies) + len(anonymous_proxies),
                "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            },
            "proxy_list": {
                "normal": normal_proxies,  # 普通代理IP列表
                "anonymous": anonymous_proxies  # 高匿代理IP列表
            }
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

        # 保存提示
        print(f"\n📁 代理IP已保存至 {filename}：")
        print(f"   ├─ 有效普通代理：{len(normal_proxies)}个")
        print(f"   ├─ 有效高匿代理：{len(anonymous_proxies)}个")
        print(f"   └─ 总计有效代理：{len(normal_proxies) + len(anonymous_proxies)}个")

    @staticmethod
    def save_to_json(filename: str, proxies: List[str]) -> None:
        """兼容方法：保存单一类型代理IP到JSON"""
        save_data = {
            "total": len(proxies),
            "update_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "proxies": proxies
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        print(f"📁 代理已保存到 {filename}，共 {len(proxies)} 个")
