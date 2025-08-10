#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫功能测试脚本
"""

import asyncio
import json
import os
import sys
from datetime import datetime

from config import CrawlerConfig
from simple_crawler import CrawlerFactory, DataStore


class TestCrawler:
    """爬虫测试类"""
    
    def __init__(self):
        self.test_results = []
    
    async def test_config_loading(self):
        """测试配置加载"""
        print("🔧 测试配置加载...")
        
        try:
            # 创建测试配置
            config = CrawlerConfig()
            config.platform = "xhs"
            config.keywords = "测试"
            config.max_items = 5
            
            # 验证配置
            if config.validate():
                print("✅ 配置验证通过")
                self.test_results.append(("配置加载", "PASS"))
            else:
                print("❌ 配置验证失败")
                self.test_results.append(("配置加载", "FAIL"))
                
        except Exception as e:
            print(f"❌ 配置加载测试失败: {e}")
            self.test_results.append(("配置加载", "FAIL"))
    
    async def test_data_store(self):
        """测试数据存储"""
        print("💾 测试数据存储...")
        
        try:
            config = CrawlerConfig()
            config.output_dir = "./test_data"
            config.save_format = "json"
            
            store = DataStore(config)
            
            # 测试数据
            test_data = {
                "platform": "test",
                "keyword": "测试",
                "title": "测试标题",
                "author": "测试作者",
                "crawl_time": datetime.now().isoformat()
            }
            
            await store.save_item(test_data)
            await store.save_to_file()
            
            # 检查文件是否创建
            if os.path.exists("./test_data"):
                print("✅ 数据存储测试通过")
                self.test_results.append(("数据存储", "PASS"))
            else:
                print("❌ 数据存储测试失败")
                self.test_results.append(("数据存储", "FAIL"))
                
        except Exception as e:
            print(f"❌ 数据存储测试失败: {e}")
            self.test_results.append(("数据存储", "FAIL"))
    
    async def test_crawler_factory(self):
        """测试爬虫工厂"""
        print("🏭 测试爬虫工厂...")
        
        try:
            config = CrawlerConfig()
            store = DataStore(config)
            
            # 测试支持的平台
            supported_platforms = ["xhs", "dy", "wb"]
            
            for platform in supported_platforms:
                try:
                    crawler = CrawlerFactory.create_crawler(platform, config, store)
                    print(f"✅ {platform} 爬虫创建成功")
                except Exception as e:
                    print(f"❌ {platform} 爬虫创建失败: {e}")
                    self.test_results.append(("爬虫工厂", "FAIL"))
                    return
            
            print("✅ 爬虫工厂测试通过")
            self.test_results.append(("爬虫工厂", "PASS"))
            
        except Exception as e:
            print(f"❌ 爬虫工厂测试失败: {e}")
            self.test_results.append(("爬虫工厂", "FAIL"))
    
    async def test_browser_launch(self):
        """测试浏览器启动"""
        print("🌐 测试浏览器启动...")
        
        try:
            from simple_crawler import BaseCrawler
            
            # 创建测试爬虫
            config = CrawlerConfig()
            config.headless = True  # 无头模式测试
            store = DataStore(config)
            
            # 使用小红书爬虫测试
            crawler = CrawlerFactory.create_crawler("xhs", config, store)
            
            # 启动浏览器
            await crawler.launch_browser()
            
            if crawler.browser and crawler.page:
                print("✅ 浏览器启动测试通过")
                self.test_results.append(("浏览器启动", "PASS"))
                
                # 清理资源
                await crawler.cleanup()
            else:
                print("❌ 浏览器启动测试失败")
                self.test_results.append(("浏览器启动", "FAIL"))
                
        except Exception as e:
            print(f"❌ 浏览器启动测试失败: {e}")
            self.test_results.append(("浏览器启动", "FAIL"))
    
    def print_test_results(self):
        """打印测试结果"""
        print("\n" + "=" * 50)
        print("📊 测试结果汇总")
        print("=" * 50)
        
        passed = 0
        failed = 0
        
        for test_name, result in self.test_results:
            status = "✅ PASS" if result == "PASS" else "❌ FAIL"
            print(f"{test_name:<15} {status}")
            
            if result == "PASS":
                passed += 1
            else:
                failed += 1
        
        print("=" * 50)
        print(f"总计: {len(self.test_results)} 项测试")
        print(f"通过: {passed} 项")
        print(f"失败: {failed} 项")
        
        if failed == 0:
            print("🎉 所有测试通过！")
        else:
            print("⚠️ 部分测试失败，请检查环境配置")
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🧪 开始运行爬虫功能测试")
        print("=" * 50)
        
        # 运行各项测试
        await self.test_config_loading()
        await self.test_data_store()
        await self.test_crawler_factory()
        await self.test_browser_launch()
        
        # 打印测试结果
        self.print_test_results()
        
        # 清理测试文件
        self.cleanup_test_files()
    
    def cleanup_test_files(self):
        """清理测试文件"""
        try:
            import shutil
            if os.path.exists("./test_data"):
                shutil.rmtree("./test_data")
                print("🧹 已清理测试文件")
        except Exception as e:
            print(f"⚠️ 清理测试文件失败: {e}")


async def main():
    """主函数"""
    print("🎯 爬虫功能测试工具")
    print("=" * 50)
    
    # 检查环境
    print("🔍 检查运行环境...")
    
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ Python 版本过低，需要 3.8 或更高版本")
        return
    
    print(f"✅ Python 版本: {sys.version}")
    
    # 检查必要文件
    required_files = ["simple_crawler.py", "config.py", "requirements.txt"]
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ 文件存在: {file}")
        else:
            print(f"❌ 文件缺失: {file}")
            return
    
    print("✅ 环境检查通过")
    print("=" * 50)
    
    # 运行测试
    tester = TestCrawler()
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 测试已中断")
    except Exception as e:
        print(f"❌ 测试运行出错: {e}")
        sys.exit(1) 