# Web应用测试文件
import unittest
import os
import tempfile
from webapp.app import app
from webapp.config import STORAGE_CONFIG

class WebAppTestCase(unittest.TestCase):
    def setUp(self):
        # 创建临时测试环境
        self.app = app.test_client()
        self.app.testing = True

        # 保存原始配置
        self.original_download_folder = STORAGE_CONFIG['DOWNLOAD_FOLDER']

        # 创建临时下载目录
        self.temp_download_folder = tempfile.mkdtemp()
        STORAGE_CONFIG['DOWNLOAD_FOLDER'] = self.temp_download_folder

    def tearDown(self):
        # 恢复原始配置
        STORAGE_CONFIG['DOWNLOAD_FOLDER'] = self.original_download_folder

        # 清理临时文件
        if os.path.exists(self.temp_download_folder):
            for file in os.listdir(self.temp_download_folder):
                os.remove(os.path.join(self.temp_download_folder, file))
            os.rmdir(self.temp_download_folder)

    def test_index_page(self):
        # 测试首页访问
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'视频爬取工具', response.data)
        self.assertIn(b'请输入视频URL', response.data)

    def test_invalid_url(self):
        # 测试无效URL
        response = self.app.post('/crawl', data={'video_url': 'invalid_url'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'无法识别视频平台或URL格式不正确', response.data)

    def test_empty_url(self):
        # 测试空URL
        response = self.app.post('/crawl', data={'video_url': ''})
        self.assertEqual(response.status_code, 302)  # 重定向

    def test_xhs_url_extraction(self):
        # 测试小红书URL提取
        from webapp.app import extract_platform_and_id
        url = 'https://www.xiaohongshu.com/explore/66fad51c000000001b0224b8?xsec_token=AB3rO-QopW5sgrJ41GwN01WCXh6yWPxjSoFI9D5JIMgKw='
        platform, params = extract_platform_and_id(url)
        self.assertEqual(platform, 'xhs')
        self.assertEqual(params['note_id'], '66fad51c000000001b0224b8')
        self.assertEqual(params['xsec_token'], 'AB3rO-QopW5sgrJ41GwN01WCXh6yWPxjSoFI9D5JIMgKw=')

    def test_dy_url_extraction(self):
        # 测试抖音URL提取
        from webapp.app import extract_platform_and_id
        url = 'https://www.douyin.com/video/7000000000000000000'
        platform, params = extract_platform_and_id(url)
        self.assertEqual(platform, 'dy')
        self.assertEqual(params['video_id'], '7000000000000000000')

if __name__ == '__main__':
    unittest.main()