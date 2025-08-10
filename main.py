#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版多平台爬虫工具 - 主程序
"""

import asyncio
import argparse
import sys
from typing import Optional

from config import CrawlerConfig, load_config_from_file, create_default_config
from simple_crawler import CrawlerFactory, DataStore


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="简化版多平台爬虫工具")
    
    parser.add_argument("--platform", "-p", 
                       choices=["xhs", "dy", "wb", "zhihu"],
                       help="爬取平台 (xhs: 小红书, dy: 抖音, wb: 微博, zhihu: 知乎)")
    
    parser.add_argument("--keywords", "-k", 
                       help="搜索关键词，多个关键词用逗号分隔")
    
    parser.add_argument("--max-items", "-m", type=int,
                       help="最大爬取数量")
    
    parser.add_argument("--headless", action="store_true",
                       help="无头模式运行")
    
    parser.add_argument("--format", "-f",
                       choices=["json", "csv", "sqlite"],
                       help="数据保存格式")
    
    parser.add_argument("--config", "-c", default="config.json",
                       help="配置文件路径")
    
    parser.add_argument("--init-config", action="store_true",
                       help="创建默认配置文件")
    
    return parser.parse_args()


def print_banner():
    """打印程序横幅"""
    banner = """
🎯 简化版多平台爬虫工具
==========================================
支持平台: 小红书(xhs) | 抖音(dy) | 微博(wb) | 知乎(zhihu)
功能特性: 关键词搜索 | 数据存储 | 登录态保存 | 代理支持
==========================================
    """
    print(banner)


def print_usage_examples():
    """打印使用示例"""
    examples = """
📖 使用示例:
==========================================
1. 使用配置文件运行:
   python main.py

2. 指定平台和关键词:
   python main.py --platform xhs --keywords "编程,Python"

3. 设置最大爬取数量:
   python main.py --platform dy --keywords "技术" --max-items 100

4. 无头模式运行:
   python main.py --platform wb --keywords "新闻" --headless

5. 指定数据保存格式:
   python main.py --platform xhs --keywords "美食" --format csv

6. 创建默认配置文件:
   python main.py --init-config

📝 配置文件说明:
- 默认配置文件: config.json
- 支持命令行参数覆盖配置文件
- 首次运行建议使用 --init-config 创建配置文件
    """
    print(examples)


async def run_crawler(config: CrawlerConfig):
    """运行爬虫"""
    print(f"🚀 开始爬取 {config.platform} 平台...")
    print(f"🔍 搜索关键词: {config.keywords}")
    print(f"📊 最大爬取数量: {config.max_items}")
    print(f"💾 数据保存格式: {config.save_format}")
    print("=" * 50)
    
    # 创建输出目录
    config.create_output_dirs()
    
    # 创建数据存储
    store = DataStore(config)
    
    # 创建并运行爬虫
    try:
        crawler = CrawlerFactory.create_crawler(config.platform, config, store)
        await crawler.start()
    except Exception as e:
        print(f"❌ 爬虫运行失败: {e}")
        return False
    
    return True


def main():
    """主函数"""
    args = parse_arguments()
    
    # 显示横幅
    print_banner()
    
    # 创建默认配置文件
    if args.init_config:
        create_default_config()
        return
    
    # 加载配置
    config = load_config_from_file(args.config)
    
    # 命令行参数覆盖配置文件
    if args.platform:
        config.platform = args.platform
    if args.keywords:
        config.keywords = args.keywords
    if args.max_items:
        config.max_items = args.max_items
    if args.headless:
        config.headless = True
    if args.format:
        config.save_format = args.format
    
    # 验证配置
    if not config.validate():
        print("\n❌ 配置验证失败，请检查参数")
        print_usage_examples()
        sys.exit(1)
    
    # 运行爬虫
    success = asyncio.run(run_crawler(config))
    
    if success:
        print("\n✅ 爬取完成！")
        print(f"📁 数据保存在: {config.output_dir}")
    else:
        print("\n❌ 爬取失败！")
        sys.exit(1)


if __name__ == "__main__":
    main() 