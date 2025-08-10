#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫配置文件
"""

import os
from dataclasses import dataclass
from typing import List


@dataclass
class CrawlerConfig:
    """爬虫配置类"""
    
    # 基础配置
    platform: str = "xhs"  # 平台：xhs, dy, wb, zhihu
    keywords: str = "编程,技术,Python"  # 搜索关键词，逗号分隔
    login_type: str = "qrcode"  # 登录方式：qrcode, cookie
    cookies: str = ""  # Cookie字符串
    
    # 爬取配置
    max_items: int = 50  # 最大爬取数量
    enable_comments: bool = True  # 是否爬取评论
    max_comments: int = 10  # 每个帖子最大评论数
    enable_images: bool = False  # 是否下载图片
    
    # 浏览器配置
    headless: bool = False  # 无头模式
    save_login_state: bool = True  # 保存登录状态
    user_data_dir: str = "./browser_data"  # 浏览器数据目录
    
    # 数据存储配置
    save_format: str = "json"  # 存储格式：json, csv, sqlite
    output_dir: str = "./data"  # 输出目录
    
    # 代理配置
    enable_proxy: bool = False
    proxy_server: str = ""
    
    # 延迟配置
    delay_between_requests: float = 1.0  # 请求间隔（秒）
    delay_between_pages: float = 2.0  # 页面间隔（秒）
    
    # 支持的平台列表
    SUPPORTED_PLATFORMS = ["xhs", "dy", "wb", "zhihu"]
    
    def validate(self) -> bool:
        """验证配置"""
        if self.platform not in self.SUPPORTED_PLATFORMS:
            print(f"❌ 不支持的平台: {self.platform}")
            print(f"✅ 支持的平台: {', '.join(self.SUPPORTED_PLATFORMS)}")
            return False
        
        if not self.keywords.strip():
            print("❌ 关键词不能为空")
            return False
        
        if self.max_items <= 0:
            print("❌ 最大爬取数量必须大于0")
            return False
        
        return True
    
    def get_keywords_list(self) -> List[str]:
        """获取关键词列表"""
        return [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
    
    def create_output_dirs(self):
        """创建输出目录"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.user_data_dir, exist_ok=True)


def load_config_from_file(config_file: str = "config.json") -> CrawlerConfig:
    """从文件加载配置"""
    if os.path.exists(config_file):
        import json
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config = CrawlerConfig()
        for key, value in config_data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config
    else:
        return CrawlerConfig()


def save_config_to_file(config: CrawlerConfig, config_file: str = "config.json"):
    """保存配置到文件"""
    import json
    
    config_data = {
        "platform": config.platform,
        "keywords": config.keywords,
        "login_type": config.login_type,
        "cookies": config.cookies,
        "max_items": config.max_items,
        "enable_comments": config.enable_comments,
        "max_comments": config.max_comments,
        "enable_images": config.enable_images,
        "headless": config.headless,
        "save_login_state": config.save_login_state,
        "user_data_dir": config.user_data_dir,
        "save_format": config.save_format,
        "output_dir": config.output_dir,
        "enable_proxy": config.enable_proxy,
        "proxy_server": config.proxy_server,
        "delay_between_requests": config.delay_between_requests,
        "delay_between_pages": config.delay_between_pages,
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置已保存到: {config_file}")


def create_default_config():
    """创建默认配置文件"""
    config = CrawlerConfig()
    save_config_to_file(config, "config.json")
    print("✅ 已创建默认配置文件: config.json")
    print("📝 请根据需要修改配置文件中的参数")


if __name__ == "__main__":
    create_default_config() 