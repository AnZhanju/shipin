# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。

import asyncio
import json
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Union
from urllib.parse import urlencode


class AbstractApiClient(ABC):
    def __init__(
        self,
        timeout=10,
        proxies=None,
        *,
        headers: Dict[str, str],
        playwright_page,
        cookie_dict: Dict[str, str],
    ):
        self.proxies = proxies
        self.timeout = timeout
        self.headers = headers
        self.playwright_page = playwright_page
        self.cookie_dict = cookie_dict
        self._host = None  # 由子类设置

    @abstractmethod
    async def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        return_response: bool = False,
    ) -> Union[Dict, str]:
        """
        发送HTTP请求
        :param method: 请求方法
        :param url: 请求URL
        :param params: 查询参数
        :param data: 表单数据
        :param json_data: JSON数据
        :param headers: 请求头
        :param return_response: 是否返回响应对象
        :return: 响应结果
        """
        pass

    @abstractmethod
    async def get(self, uri: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """发送GET请求"""
        pass

    @abstractmethod
    async def post(self, uri: str, data: dict, headers: Optional[Dict] = None) -> Dict:
        """发送POST请求"""
        pass

    @abstractmethod
    async def pong(self, browser_context) -> bool:
        """检查登录状态"""
        pass

    @abstractmethod
    async def get_note_info_by_id(self, note_id: str) -> Dict:
        """
        根据ID获取笔记/视频详情
        :param note_id: 笔记/视频ID
        :return: 笔记/视频信息
        """
        pass

    @abstractmethod
    async def get_note_media(self, media_url: str) -> bytes:
        """
        下载媒体文件
        :param media_url: 媒体URL
        :return: 媒体内容
        """
        pass

    # 以下是通用工具方法
    async def update_cookies(self, new_cookies: List[Dict]) -> None:
        """更新cookies"""
        for cookie in new_cookies:
            self.cookie_dict[cookie['name']] = cookie['value']
        # 更新headers中的cookie
        cookie_str = '; '.join([f'{k}={v}' for k, v in self.cookie_dict.items()])
        self.headers['Cookie'] = cookie_str

    def _extract_cookies(self, response_headers: Dict) -> Dict:
        """从响应头中提取cookies"""
        cookies = {}
        if 'Set-Cookie' in response_headers:
            cookie_headers = response_headers['Set-Cookie']
            if isinstance(cookie_headers, str):
                cookie_headers = [cookie_headers]
            for cookie_header in cookie_headers:
                parts = cookie_header.split(';')
                cookie_name_value = parts[0].strip()
                if '=' in cookie_name_value:
                    name, value = cookie_name_value.split('=', 1)
                    cookies[name] = value
        return cookies