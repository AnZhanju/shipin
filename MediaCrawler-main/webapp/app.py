# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。

import os
import re
import asyncio
import requests
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from media_platform.xhs.client import XiaoHongShuClient
from media_platform.douyin.client import DOUYINClient
from media_platform.weibo.client import WeiboClient
from media_platform.toutiao.client import TouTiaoClient
from tools import utils
import config

# 设置模板目录的绝对路径
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'MediaCrawler-main', 'templates'))
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 确保下载目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 支持的平台
SUPPORTED_PLATFORMS = {
    'xhs': '小红书',
    'dy': '抖音',
    'wb': '新浪',
    'tt': '头条',
}

# 从URL提取平台类型和ID
def extract_platform_and_id(url):
    # 小红书URL格式: https://www.xiaohongshu.com/explore/66fad51c000000001b0224b8?xsec_token=...
    xhs_match = re.search(r'xiaohongshu\.com/explore/(\w+)', url)
    if xhs_match:
        note_id = xhs_match.group(1)
        # 提取xsec_token
        xsec_token_match = re.search(r'xsec_token=(\w+)', url)
        xsec_token = xsec_token_match.group(1) if xsec_token_match else ''
        return 'xhs', {'note_id': note_id, 'xsec_token': xsec_token}

    # 抖音URL格式: https://www.douyin.com/video/7000000000000000000
    dy_match = re.search(r'douyin\.com/video/(\d+)', url)
    if dy_match:
        video_id = dy_match.group(1)
        return 'dy', {'video_id': video_id}

    # 新浪URL格式: https://m.weibo.cn/detail/1234567890
    wb_match = re.search(r'weibo\.cn/detail/(\d+)', url)
    if wb_match:
        note_id = wb_match.group(1)
        return 'wb', {'note_id': note_id}

    # 头条URL格式: https://www.toutiao.com/video/1234567890
    tt_match = re.search(r'toutiao\.com/video/(\d+)', url)
    if tt_match:
        video_id = tt_match.group(1)
        return 'tt', {'video_id': video_id}

    return None, None

# 异步爬取视频的函数
async def crawl_video(platform, params):
    try:
        if platform == 'xhs':
            # 这里使用项目现有的小红书客户端
            # 注意：实际使用时需要初始化浏览器上下文等
            from playwright.async_api import async_playwright
            async with async_playwright() as playwright:
                chromium = playwright.chromium
                browser = await chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto('https://www.xiaohongshu.com')
                
                # 获取cookies
                cookie_str, cookie_dict = utils.convert_cookies(await context.cookies())
                
                # 初始化客户端
                client = XiaoHongShuClient(
                    headers={
                        'User-Agent': await page.evaluate('() => navigator.userAgent'),
                        'Cookie': cookie_str,
                    },
                    playwright_page=page,
                    cookie_dict=cookie_dict
                )
                
                # 获取笔记详情
                note_id = params['note_id']
                xsec_token = params['xsec_token']
                note_info = await client.get_note_by_id(note_id, 'pc_search', xsec_token)
                
                # 提取视频URL
                if note_info and 'video' in note_info:
                    video_url = note_info['video']['media']['url_list'][0]
                    
                    # 下载视频
                    video_content = await client.get_note_media(video_url)
                    if video_content:
                        filename = secure_filename(f'xhs_{note_id}.mp4')
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        with open(filepath, 'wb') as f:
                            f.write(video_content)
                        return {'success': True, 'filepath': filepath, 'note_info': note_info}
                    else:
                        return {'success': False, 'error': '无法下载视频'}
                else:
                    return {'success': False, 'error': '未找到视频信息'}

        elif platform == 'dy':
            # 抖音爬取逻辑
            from playwright.async_api import async_playwright
            async with async_playwright() as playwright:
                chromium = playwright.chromium
                browser = await chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto('https://www.douyin.com')
                
                # 获取cookies
                cookie_str, cookie_dict = utils.convert_cookies(await context.cookies())
                
                # 初始化客户端
                client = DOUYINClient(
                    headers={
                        'User-Agent': await page.evaluate('() => navigator.userAgent'),
                        'Cookie': cookie_str,
                    },
                    playwright_page=page,
                    cookie_dict=cookie_dict
                )
                
                # 获取视频详情
                video_id = params['video_id']
                video_info = await client.get_video_by_id(video_id)
                
                # 提取视频URL
                if video_info and 'video' in video_info:
                    video_url = video_info['video']['play_addr']['url_list'][0]
                    
                    # 下载视频
                    response = requests.get(video_url, stream=True)
                    if response.status_code == 200:
                        filename = secure_filename(f'dy_{video_id}.mp4')
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                        return {'success': True, 'filepath': filepath, 'video_info': video_info}
                    else:
                        return {'success': False, 'error': '无法下载视频'}
                else:
                    return {'success': False, 'error': '未找到视频信息'}

        elif platform == 'wb':
            # 新浪爬取逻辑
            from playwright.async_api import async_playwright
            async with async_playwright() as playwright:
                chromium = playwright.chromium
                browser = await chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto('https://m.weibo.cn')
                
                # 获取cookies
                cookie_str, cookie_dict = utils.convert_cookies(await context.cookies())
                
                # 初始化客户端
                client = WeiboClient(
                    headers={
                        'User-Agent': await page.evaluate('() => navigator.userAgent'),
                        'Cookie': cookie_str,
                    },
                    playwright_page=page,
                    cookie_dict=cookie_dict
                )
                
                # 获取微博详情
                note_id = params['note_id']
                note_info = await client.get_note_info_by_id(note_id)
                
                # 提取视频URL
                if note_info and 'page_info' in note_info and 'media_info' in note_info['page_info']:
                    video_url = note_info['page_info']['media_info']['stream_url']
                    
                    # 下载视频
                    response = requests.get(video_url, stream=True)
                    if response.status_code == 200:
                        filename = secure_filename(f'wb_{note_id}.mp4')
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=1024):
                                if chunk:
                                    f.write(chunk)
                        return {'success': True, 'filepath': filepath, 'note_info': note_info}
                    else:
                        return {'success': False, 'error': '无法下载视频'}
                else:
                    return {'success': False, 'error': '未找到视频信息'}
        elif platform == 'tt':
            # 头条爬取逻辑
            from playwright.async_api import async_playwright
            async with async_playwright() as playwright:
                chromium = playwright.chromium
                browser = await chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto('https://www.toutiao.com')
                
                # 获取cookies
                cookie_str, cookie_dict = utils.convert_cookies(await context.cookies())
                
                # 初始化客户端
                client = TouTiaoClient(
                    headers={
                        'User-Agent': await page.evaluate('() => navigator.userAgent'),
                        'Cookie': cookie_str,
                    },
                    playwright_page=page,
                    cookie_dict=cookie_dict
                )
                
                # 获取头条视频详情
                note_id = params['video_id']
                video_info = await client.get_note_info_by_id(note_id)
                
                # 提取视频URL
                # 注意：这里需要根据头条API的实际返回结构调整
                if video_info and 'data' in video_info and 'video_list' in video_info['data']:
                    # 选择最高质量的视频
                    video_list = video_info['data']['video_list']
                    if video_list:
                        # 假设video_list按质量排序，选择第一个
                        best_video = video_list[0]
                        video_url = best_video.get('main_url', '')
                        
                        if video_url:
                            # 下载视频
                            video_content = await client.get_note_media(video_url)
                            if video_content:
                                filename = secure_filename(f'tt_{note_id}.mp4')
                                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                                with open(filepath, 'wb') as f:
                                    f.write(video_content)
                                return {'success': True, 'filepath': filepath, 'note_info': video_info}
                            else:
                                return {'success': False, 'error': '无法下载视频'}
                        else:
                            return {'success': False, 'error': '未找到视频URL'}
                    else:
                        return {'success': False, 'error': '视频列表为空'}
                else:
                    return {'success': False, 'error': '未找到视频信息'}
        else:
            return {'success': False, 'error': '不支持的平台'}

    except Exception as e:
        utils.logger.error(f'爬取视频失败: {e}')
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html', supported_platforms=SUPPORTED_PLATFORMS)

@app.route('/crawl', methods=['POST'])
def crawl():
    video_url = request.form.get('video_url')
    if not video_url:
        flash('请输入视频URL')
        return redirect(url_for('index'))

    platform, params = extract_platform_and_id(video_url)
    if not platform:
        flash('无法识别视频平台或URL格式不正确')
        return redirect(url_for('index'))

    if platform not in SUPPORTED_PLATFORMS:
        flash(f'暂不支持{SUPPORTED_PLATFORMS.get(platform, platform)}平台')
        return redirect(url_for('index'))

    # 运行异步爬取任务
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(crawl_video(platform, params))
    loop.close()

    if result['success']:
        flash('视频爬取成功')
        return jsonify({
            'success': True,
            'filepath': result['filepath'],
            'note_info': result['note_info']
        })
    else:
        flash(f'视频爬取失败: {result.get("error", "未知错误")}')
        return jsonify({
            'success': False,
            'error': result.get("error", "未知错误")
        })

@app.route('/download/<filename>')
def download_file(filename):
    return redirect(url_for('static', filename=f'downloads/{filename}'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # 确保templates目录存在
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
    os.makedirs(template_dir, exist_ok=True)
    app.run(debug=True)