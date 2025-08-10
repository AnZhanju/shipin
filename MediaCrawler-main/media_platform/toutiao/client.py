# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。

import asyncio
import json
from typing import Any, Callable, Dict, List, Optional, Union
from urllib.parse import urlencode

from tools import utils
from media_platform.base.client import AbstractApiClient


class TouTiaoClient(AbstractApiClient):
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
        self._host = "https://www.toutiao.com"
        self.playwright_page = playwright_page
        self.cookie_dict = cookie_dict

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
        try:
            headers = headers or self.headers
            response = await utils.async_request(
                method,
                url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
                proxies=self.proxies,
            )

            if return_response:
                return response.text

            if response.status_code != 200:
                utils.logger.error(f"请求失败: {response.status_code}, {response.text}")
                return {}

            try:
                return response.json()
            except json.JSONDecodeError:
                utils.logger.error(f"响应不是有效的JSON: {response.text}")
                return {}
        except Exception as e:
            utils.logger.error(f"请求异常: {e}")
            return {}

    async def get(self, uri: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """发送GET请求"""
        url = f"{self._host}{uri}"
        if params:
            url += f"?{urlencode(params)}"
        return await self.request(method="GET", url=url, headers=headers)

    async def post(self, uri: str, data: dict, headers: Optional[Dict] = None) -> Dict:
        """发送POST请求"""
        return await self.request(method="POST", url=f"{self._host}{uri}", data=data, headers=headers)

    async def pong(self, browser_context) -> bool:
        """检查登录状态"""
        try:
            response = await self.get("/api/ping")
            return response.get("success", False)
        except Exception as e:
            utils.logger.error(f"检查登录状态失败: {e}")
            return False

    async def get_note_info_by_id(self, note_id: str) -> Dict:
        """
        根据ID获取视频详情
        :param note_id: 视频ID
        :return: 视频信息
        """
        try:
            # 头条视频详情API
            response = await self.get(f"/video/{note_id}")
            return response
        except Exception as e:
            utils.logger.error(f"获取视频详情失败: {e}")
            return {}

    async def get_note_media(self, media_url: str) -> bytes:
        """
        下载视频媒体文件
        :param media_url: 视频URL
        :return: 视频内容
        """
        try:
            response = await utils.async_request(
                "GET",
                media_url,
                headers=self.headers,
                timeout=self.timeout,
                proxies=self.proxies,
                stream=True,
            )

            if response.status_code != 200:
                utils.logger.error(f"下载视频失败: {response.status_code}")
                return b""

            content = b""
            async for chunk in response.aiter_content(chunk_size=1024):
                if chunk:
                    content += chunk
            return content
        except Exception as e:
            utils.logger.error(f"下载视频异常: {e}")
            return b""