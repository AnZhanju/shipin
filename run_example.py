#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫工具使用示例
"""

import asyncio
import sys
from config import CrawlerConfig
from simple_crawler import CrawlerFactory, DataStore


async def example_xiaohongshu():
    """小红书爬取示例"""
    print("🎯 小红书爬取示例")
    print("=" * 50)
    
    # 创建配置
    config = CrawlerConfig()
    config.platform = "xhs"
    config.keywords = "编程,Python"
    config.max_items = 10
    config.save_format = "json"
    config.headless = False  # 显示浏览器便于调试
    
    # 创建数据存储
    store = DataStore(config)
    
    # 创建爬虫并运行
    crawler = CrawlerFactory.create_crawler("xhs", config, store)
    await crawler.start()


async def example_douyin():
    """抖音爬取示例"""
    print("🎯 抖音爬取示例")
    print("=" * 50)
    
    # 创建配置
    config = CrawlerConfig()
    config.platform = "dy"
    config.keywords = "技术,编程"
    config.max_items = 10
    config.save_format = "json"
    config.headless = False
    
    # 创建数据存储
    store = DataStore(config)
    
    # 创建爬虫并运行
    crawler = CrawlerFactory.create_crawler("dy", config, store)
    await crawler.start()


async def example_weibo():
    """微博爬取示例"""
    print("🎯 微博爬取示例")
    print("=" * 50)
    
    # 创建配置
    config = CrawlerConfig()
    config.platform = "wb"
    config.keywords = "新闻,热点"
    config.max_items = 10
    config.save_format = "json"
    config.headless = False
    
    # 创建数据存储
    store = DataStore(config)
    
    # 创建爬虫并运行
    crawler = CrawlerFactory.create_crawler("wb", config, store)
    await crawler.start()


def print_menu():
    """打印菜单"""
    menu = """
🎯 爬虫工具使用示例
==========================================
请选择要运行的示例:

1. 小红书爬取示例
2. 抖音爬取示例  
3. 微博爬取示例
4. 退出

请输入选项 (1-4): """
    return input(menu)


async def main():
    """主函数"""
    print("🎯 爬虫工具使用示例")
    print("=" * 50)
    
    while True:
        choice = print_menu()
        
        if choice == "1":
            await example_xiaohongshu()
        elif choice == "2":
            await example_douyin()
        elif choice == "3":
            await example_weibo()
        elif choice == "4":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选项，请重新选择")
        
        print("\n" + "=" * 50)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"❌ 程序运行出错: {e}")
        sys.exit(1) 