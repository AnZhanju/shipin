# 🚀 安装和使用指南

## 📋 环境要求

- Python 3.8 或更高版本
- Windows 10/11, macOS, 或 Linux
- 稳定的网络连接

## 🔧 安装步骤

### 1. 克隆或下载项目

```bash
# 如果使用 Git
git clone <项目地址>
cd simple-crawler

# 或者直接下载项目文件
```

### 2. 安装 Python 依赖

```bash
# 安装依赖包
pip install -r requirements.txt
```

### 3. 安装浏览器驱动

```bash
# 安装 Playwright 浏览器驱动
playwright install
```

### 4. 创建配置文件

```bash
# 创建默认配置文件
python main.py --init-config
```

## 🎯 快速开始

### 方法一：使用配置文件

1. **编辑配置文件**
   ```bash
   # 编辑 config.json 文件
   {
     "platform": "xhs",
     "keywords": "编程,Python",
     "max_items": 20,
     "headless": false
   }
   ```

2. **运行爬虫**
   ```bash
   python main.py
   ```

### 方法二：使用命令行参数

```bash
# 爬取小红书
python main.py --platform xhs --keywords "编程,Python" --max-items 20

# 爬取抖音
python main.py --platform dy --keywords "技术" --max-items 30

# 爬取微博
python main.py --platform wb --keywords "新闻" --max-items 25

# 无头模式运行
python main.py --platform xhs --keywords "美食" --headless
```

### 方法三：使用示例脚本

```bash
# 运行交互式示例
python run_example.py
```

## 📖 详细使用说明

### 支持的平台

| 平台代码 | 平台名称 | 支持功能 |
|---------|---------|---------|
| xhs | 小红书 | 笔记搜索、数据提取 |
| dy | 抖音 | 视频搜索、数据提取 |
| wb | 微博 | 微博搜索、数据提取 |
| zhihu | 知乎 | 问答搜索、数据提取 |

### 配置参数说明

#### 基础配置
- `platform`: 爬取平台 (xhs, dy, wb, zhihu)
- `keywords`: 搜索关键词，多个关键词用逗号分隔
- `login_type`: 登录方式 (qrcode, cookie)
- `max_items`: 最大爬取数量

#### 浏览器配置
- `headless`: 无头模式 (true/false)
- `save_login_state`: 保存登录状态 (true/false)
- `user_data_dir`: 浏览器数据目录

#### 数据存储配置
- `save_format`: 数据保存格式 (json, csv, sqlite)
- `output_dir`: 输出目录

#### 代理配置
- `enable_proxy`: 启用代理 (true/false)
- `proxy_server`: 代理服务器地址

#### 延迟配置
- `delay_between_requests`: 请求间隔（秒）
- `delay_between_pages`: 页面间隔（秒）

### 数据输出格式

#### JSON 格式示例
```json
{
  "platform": "xiaohongshu",
  "keyword": "编程",
  "title": "Python入门教程",
  "author": "编程小助手",
  "link": "https://www.xiaohongshu.com/...",
  "likes": "1234",
  "crawl_time": "2024-01-01T12:00:00"
}
```

#### CSV 格式示例
```csv
platform,keyword,title,author,link,likes,crawl_time
xiaohongshu,编程,Python入门教程,编程小助手,https://...,1234,2024-01-01T12:00:00
```

## 🔍 常见问题

### Q: 登录失败怎么办？
A: 
1. 确保网络连接正常
2. 尝试关闭无头模式 (`headless: false`)
3. 手动完成验证码验证
4. 检查是否被平台限制

### Q: 爬取速度很慢？
A:
1. 调整 `delay_between_requests` 参数
2. 减少 `max_items` 数量
3. 使用代理服务器
4. 检查网络连接

### Q: 数据没有保存？
A:
1. 检查 `output_dir` 目录权限
2. 确认 `save_format` 设置正确
3. 查看控制台错误信息

### Q: 浏览器启动失败？
A:
1. 重新安装 Playwright: `playwright install`
2. 检查系统防火墙设置
3. 尝试使用不同的浏览器参数

## ⚠️ 注意事项

### 法律合规
- 仅用于学习和研究目的
- 遵守目标平台的robots.txt规则
- 合理控制请求频率
- 不得用于商业用途

### 技术限制
- 部分平台可能有反爬虫机制
- 需要手动处理验证码
- 登录状态可能过期
- 网站结构变化可能影响爬取

### 性能优化
- 使用代理池轮换IP
- 合理设置延迟时间
- 避免同时运行多个爬虫
- 定期清理浏览器缓存

## 🛠️ 故障排除

### 错误日志查看
```bash
# 查看详细错误信息
python main.py --platform xhs --keywords "测试" 2>&1 | tee error.log
```

### 调试模式
```bash
# 关闭无头模式进行调试
python main.py --platform xhs --keywords "测试" --headless false
```

### 清理缓存
```bash
# 删除浏览器数据目录
rm -rf browser_data/
```

## 📞 技术支持

如果遇到问题，请：

1. 查看错误日志
2. 检查配置文件
3. 尝试简化测试用例
4. 参考项目文档

---

**免责声明**: 本工具仅供学习和研究使用，使用者应自行承担使用风险。 