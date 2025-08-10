#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版多平台爬虫工具
支持：小红书、抖音、微博、知乎等平台
仅供学习和研究使用
"""

import asyncio
import json
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin

import aiofiles
from playwright.async_api import async_playwright, Browser, BrowserContext, Page


class Config:
    """配置管理类"""
    
    def __init__(self):
        # 基础配置
        self.platform = "xhs"  # 平台：xhs, dy, wb, zhihu
        self.keywords = "编程,技术"  # 搜索关键词
        self.login_type = "qrcode"  # 登录方式：qrcode, cookie
        self.cookies = ""  # Cookie字符串
        
        # 爬取配置
        self.max_items = 50  # 最大爬取数量
        self.enable_comments = True  # 是否爬取评论
        self.max_comments = 10  # 每个帖子最大评论数
        self.enable_images = False  # 是否下载图片
        
        # 浏览器配置
        self.headless = False  # 无头模式
        self.save_login_state = True  # 保存登录状态
        self.user_data_dir = "./browser_data"  # 浏览器数据目录
        
        # 数据存储配置
        self.save_format = "json"  # 存储格式：json, csv, sqlite
        self.output_dir = "./data"  # 输出目录
        
        # 代理配置
        self.enable_proxy = False
        self.proxy_server = ""
        
        # 延迟配置
        self.delay_between_requests = 1  # 请求间隔（秒）
        self.delay_between_pages = 2  # 页面间隔（秒）


class DataStore:
    """数据存储类"""
    
    def __init__(self, config: Config):
        self.config = config
        self.output_dir = config.output_dir
        self.data = []
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def save_item(self, item: Dict):
        """保存单个数据项"""
        self.data.append(item)
    
    async def save_to_file(self):
        """保存数据到文件"""
        if not self.data:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        platform = self.config.platform
        
        if self.config.save_format == "json":
            filename = f"{platform}_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(self.data, ensure_ascii=False, indent=2))
            
            print(f"✅ 数据已保存到: {filepath}")
            print(f"📊 共保存 {len(self.data)} 条数据")
        
        elif self.config.save_format == "csv":
            import csv
            filename = f"{platform}_{timestamp}.csv"
            filepath = os.path.join(self.output_dir, filename)
            
            if self.data:
                fieldnames = self.data[0].keys()
                with open(filepath, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(self.data)
                
                print(f"✅ 数据已保存到: {filepath}")
                print(f"📊 共保存 {len(self.data)} 条数据")


class BaseCrawler(ABC):
    """爬虫基类"""
    
    def __init__(self, config: Config, store: DataStore):
        self.config = config
        self.store = store
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def start(self):
        """启动爬虫"""
        try:
            print(f"🚀 开始爬取 {self.config.platform} 平台...")
            
            # 启动浏览器
            await self.launch_browser()
            
            # 登录
            await self.login()
            
            # 执行爬取
            await self.crawl()
            
        except Exception as e:
            print(f"❌ 爬取过程中出现错误: {e}")
        finally:
            await self.cleanup()
    
    async def launch_browser(self):
        """启动浏览器"""
        playwright = await async_playwright().start()
        
        # 浏览器启动参数
        browser_args = [
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage'
        ]
        
        # 代理配置
        proxy = None
        if self.config.enable_proxy and self.config.proxy_server:
            proxy = {"server": self.config.proxy_server}
        
        # 启动浏览器
        self.browser = await playwright.chromium.launch(
            headless=self.config.headless,
            args=browser_args,
            proxy=proxy
        )
        
        # 创建上下文
        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        if self.config.save_login_state:
            context_options["user_data_dir"] = os.path.join(
                self.config.user_data_dir, 
                self.config.platform
            )
        
        self.context = await self.browser.new_context(**context_options)
        self.page = await self.context.new_page()
        
        print("✅ 浏览器启动成功")
    
    @abstractmethod
    async def login(self):
        """登录方法，子类必须实现"""
        pass
    
    @abstractmethod
    async def crawl(self):
        """爬取方法，子类必须实现"""
        pass
    
    async def cleanup(self):
        """清理资源"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        
        # 保存数据
        await self.store.save_to_file()
        print("✅ 爬取完成")


class XiaoHongShuCrawler(BaseCrawler):
    """小红书爬虫"""
    
    async def login(self):
        """小红书登录"""
        print("🔐 正在登录小红书...")
        
        await self.page.goto("https://www.xiaohongshu.com")
        await self.page.wait_for_load_state("networkidle")
        
        if self.config.login_type == "qrcode":
            # 等待用户扫码登录
            print("📱 请使用小红书APP扫描二维码登录...")
            
            # 等待登录成功
            try:
                await self.page.wait_for_selector('[data-testid="user-avatar"]', timeout=300000)
                print("✅ 登录成功")
            except Exception as e:
                print("❌ 登录超时或失败")
                raise e
    
    async def crawl(self):
        """爬取小红书内容"""
        print("🔍 开始搜索关键词...")
        
        for keyword in self.config.keywords.split(','):
            keyword = keyword.strip()
            if not keyword:
                continue
            
            print(f"🔍 搜索关键词: {keyword}")
            
            # 搜索页面
            search_url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}"
            await self.page.goto(search_url)
            await self.page.wait_for_load_state("networkidle")
            
            # 爬取搜索结果
            await self.crawl_search_results(keyword)
            
            # 页面间隔
            await asyncio.sleep(self.config.delay_between_pages)
    
    async def crawl_search_results(self, keyword: str):
        """爬取搜索结果"""
        items_count = 0
        
        while items_count < self.config.max_items:
            # 获取笔记列表
            notes = await self.page.query_selector_all('[data-testid="note-item"]')
            
            for note in notes:
                if items_count >= self.config.max_items:
                    break
                
                try:
                    # 提取笔记信息
                    note_data = await self.extract_note_data(note, keyword)
                    if note_data:
                        await self.store.save_item(note_data)
                        items_count += 1
                        print(f"📝 已爬取 {items_count} 条笔记")
                    
                    await asyncio.sleep(self.config.delay_between_requests)
                    
                except Exception as e:
                    print(f"⚠️ 提取笔记数据失败: {e}")
                    continue
            
            # 尝试翻页
            try:
                next_button = await self.page.query_selector('[data-testid="next-page"]')
                if next_button:
                    await next_button.click()
                    await self.page.wait_for_load_state("networkidle")
                else:
                    break
            except:
                break
    
    async def extract_note_data(self, note_element, keyword: str) -> Optional[Dict]:
        """提取笔记数据"""
        try:
            # 提取标题
            title_element = await note_element.query_selector('[data-testid="note-title"]')
            title = await title_element.text_content() if title_element else ""
            
            # 提取链接
            link_element = await note_element.query_selector('a')
            link = await link_element.get_attribute('href') if link_element else ""
            if link and not link.startswith('http'):
                link = urljoin("https://www.xiaohongshu.com", link)
            
            # 提取作者
            author_element = await note_element.query_selector('[data-testid="author-name"]')
            author = await author_element.text_content() if author_element else ""
            
            # 提取点赞数
            like_element = await note_element.query_selector('[data-testid="like-count"]')
            likes = await like_element.text_content() if like_element else "0"
            
            return {
                "platform": "xiaohongshu",
                "keyword": keyword,
                "title": title.strip() if title else "",
                "author": author.strip() if author else "",
                "link": link,
                "likes": likes.strip() if likes else "0",
                "crawl_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ 提取笔记数据失败: {e}")
            return None


class DouYinCrawler(BaseCrawler):
    """抖音爬虫"""
    
    async def login(self):
        """抖音登录"""
        print("🔐 正在登录抖音...")
        
        await self.page.goto("https://www.douyin.com")
        await self.page.wait_for_load_state("networkidle")
        
        if self.config.login_type == "qrcode":
            print("📱 请使用抖音APP扫描二维码登录...")
            
            try:
                await self.page.wait_for_selector('.avatar', timeout=300000)
                print("✅ 登录成功")
            except Exception as e:
                print("❌ 登录超时或失败")
                raise e
    
    async def crawl(self):
        """爬取抖音内容"""
        print("🔍 开始搜索关键词...")
        
        for keyword in self.config.keywords.split(','):
            keyword = keyword.strip()
            if not keyword:
                continue
            
            print(f"🔍 搜索关键词: {keyword}")
            
            # 搜索页面
            search_url = f"https://www.douyin.com/search/{keyword}"
            await self.page.goto(search_url)
            await self.page.wait_for_load_state("networkidle")
            
            # 爬取搜索结果
            await self.crawl_search_results(keyword)
            
            await asyncio.sleep(self.config.delay_between_pages)
    
    async def crawl_search_results(self, keyword: str):
        """爬取搜索结果"""
        items_count = 0
        
        while items_count < self.config.max_items:
            # 获取视频列表
            videos = await self.page.query_selector_all('[data-e2e="scroll-item"]')
            
            for video in videos:
                if items_count >= self.config.max_items:
                    break
                
                try:
                    video_data = await self.extract_video_data(video, keyword)
                    if video_data:
                        await self.store.save_item(video_data)
                        items_count += 1
                        print(f"🎬 已爬取 {items_count} 个视频")
                    
                    await asyncio.sleep(self.config.delay_between_requests)
                    
                except Exception as e:
                    print(f"⚠️ 提取视频数据失败: {e}")
                    continue
            
            # 滚动加载更多
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.page.wait_for_timeout(2000)
    
    async def extract_video_data(self, video_element, keyword: str) -> Optional[Dict]:
        """提取视频数据"""
        try:
            # 提取标题
            title_element = await video_element.query_selector('[data-e2e="video-title"]')
            title = await title_element.text_content() if title_element else ""
            
            # 提取作者
            author_element = await video_element.query_selector('[data-e2e="video-author"]')
            author = await author_element.text_content() if author_element else ""
            
            # 提取点赞数
            like_element = await video_element.query_selector('[data-e2e="like-count"]')
            likes = await like_element.text_content() if like_element else "0"
            
            # 提取链接
            link_element = await video_element.query_selector('a')
            link = await link_element.get_attribute('href') if link_element else ""
            if link and not link.startswith('http'):
                link = urljoin("https://www.douyin.com", link)
            
            return {
                "platform": "douyin",
                "keyword": keyword,
                "title": title.strip() if title else "",
                "author": author.strip() if author else "",
                "link": link,
                "likes": likes.strip() if likes else "0",
                "crawl_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ 提取视频数据失败: {e}")
            return None


class WeiboCrawler(BaseCrawler):
    """微博爬虫"""
    
    async def login(self):
        """微博登录"""
        print("🔐 正在登录微博...")
        
        await self.page.goto("https://weibo.com")
        await self.page.wait_for_load_state("networkidle")
        
        if self.config.login_type == "qrcode":
            print("📱 请使用微博APP扫描二维码登录...")
            
            try:
                await self.page.wait_for_selector('.avatar', timeout=300000)
                print("✅ 登录成功")
            except Exception as e:
                print("❌ 登录超时或失败")
                raise e
    
    async def crawl(self):
        """爬取微博内容"""
        print("🔍 开始搜索关键词...")
        
        for keyword in self.config.keywords.split(','):
            keyword = keyword.strip()
            if not keyword:
                continue
            
            print(f"🔍 搜索关键词: {keyword}")
            
            # 搜索页面
            search_url = f"https://s.weibo.com/weibo?q={keyword}"
            await self.page.goto(search_url)
            await self.page.wait_for_load_state("networkidle")
            
            # 爬取搜索结果
            await self.crawl_search_results(keyword)
            
            await asyncio.sleep(self.config.delay_between_pages)
    
    async def crawl_search_results(self, keyword: str):
        """爬取搜索结果"""
        items_count = 0
        
        while items_count < self.config.max_items:
            # 获取微博列表
            weibos = await self.page.query_selector_all('.card-wrap')
            
            for weibo in weibos:
                if items_count >= self.config.max_items:
                    break
                
                try:
                    weibo_data = await self.extract_weibo_data(weibo, keyword)
                    if weibo_data:
                        await self.store.save_item(weibo_data)
                        items_count += 1
                        print(f"📝 已爬取 {items_count} 条微博")
                    
                    await asyncio.sleep(self.config.delay_between_requests)
                    
                except Exception as e:
                    print(f"⚠️ 提取微博数据失败: {e}")
                    continue
            
            # 翻页
            try:
                next_button = await self.page.query_selector('.next')
                if next_button:
                    await next_button.click()
                    await self.page.wait_for_load_state("networkidle")
                else:
                    break
            except:
                break
    
    async def extract_weibo_data(self, weibo_element, keyword: str) -> Optional[Dict]:
        """提取微博数据"""
        try:
            # 提取内容
            content_element = await weibo_element.query_selector('.txt')
            content = await content_element.text_content() if content_element else ""
            
            # 提取作者
            author_element = await weibo_element.query_selector('.name')
            author = await author_element.text_content() if author_element else ""
            
            # 提取时间
            time_element = await weibo_element.query_selector('.from')
            time_str = await time_element.text_content() if time_element else ""
            
            # 提取转发数
            forward_element = await weibo_element.query_selector('.card-act li:nth-child(2)')
            forwards = await forward_element.text_content() if forward_element else "0"
            
            # 提取评论数
            comment_element = await weibo_element.query_selector('.card-act li:nth-child(3)')
            comments = await comment_element.text_content() if comment_element else "0"
            
            # 提取点赞数
            like_element = await weibo_element.query_selector('.card-act li:nth-child(4)')
            likes = await like_element.text_content() if like_element else "0"
            
            return {
                "platform": "weibo",
                "keyword": keyword,
                "content": content.strip() if content else "",
                "author": author.strip() if author else "",
                "time": time_str.strip() if time_str else "",
                "forwards": forwards.strip() if forwards else "0",
                "comments": comments.strip() if comments else "0",
                "likes": likes.strip() if likes else "0",
                "crawl_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"⚠️ 提取微博数据失败: {e}")
            return None


class CrawlerFactory:
    """爬虫工厂类"""
    
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "wb": WeiboCrawler,
    }
    
    @staticmethod
    def create_crawler(platform: str, config: Config, store: DataStore):
        """创建爬虫实例"""
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError(f"不支持的平台: {platform}")
        return crawler_class(config, store)


async def main():
    """主函数"""
    print("🎯 简化版多平台爬虫工具")
    print("=" * 50)
    
    # 创建配置
    config = Config()
    
    # 创建数据存储
    store = DataStore(config)
    
    # 创建爬虫
    try:
        crawler = CrawlerFactory.create_crawler(config.platform, config, store)
        await crawler.start()
    except Exception as e:
        print(f"❌ 爬虫启动失败: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 