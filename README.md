# 🎯 简化版多平台爬虫工具

一个功能强大的多平台自媒体数据采集工具，支持小红书、抖音、微博、知乎等主流平台的公开信息抓取。

## ✨ 功能特性

| 平台   | 关键词搜索 | 数据存储 | 登录态保存 | 代理支持 |
| ------ | ---------- | -------- | ---------- | -------- |
| 小红书 | ✅          | ✅        | ✅          | ✅        |
| 抖音   | ✅          | ✅        | ✅          | ✅        |
| 微博   | ✅          | ✅        | ✅          | ✅        |
| 知乎   | ✅          | ✅        | ✅          | ✅        |

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装 Python 3.8+
# 安装依赖
pip install -r requirements.txt

# 安装浏览器驱动
playwright install
```

### 2. 创建配置文件

```bash
python main.py --init-config
```

这将创建默认的 `config.json` 配置文件。

### 3. 运行爬虫

```bash
# 使用配置文件运行
python main.py

# 指定平台和关键词
python main.py --platform xhs --keywords "编程,Python"

# 设置最大爬取数量
python main.py --platform dy --keywords "技术" --max-items 100

# 无头模式运行
python main.py --platform wb --keywords "新闻" --headless
```

## 📖 使用说明

### 命令行参数

- `--platform, -p`: 爬取平台 (xhs, dy, wb, zhihu)
- `--keywords, -k`: 搜索关键词，多个关键词用逗号分隔
- `--max-items, -m`: 最大爬取数量
- `--headless`: 无头模式运行
- `--format, -f`: 数据保存格式 (json, csv, sqlite)
- `--config, -c`: 配置文件路径
- `--init-config`: 创建默认配置文件

### 配置文件说明

```json
{
  "platform": "xhs",
  "keywords": "编程,技术,Python",
  "login_type": "qrcode",
  "max_items": 50,
  "enable_comments": true,
  "max_comments": 10,
  "enable_images": false,
  "headless": false,
  "save_login_state": true,
  "user_data_dir": "./browser_data",
  "save_format": "json",
  "output_dir": "./data",
  "enable_proxy": false,
  "proxy_server": "",
  "delay_between_requests": 1.0,
  "delay_between_pages": 2.0
}
```

## 📁 项目结构

```
├── main.py              # 主程序
├── simple_crawler.py    # 爬虫核心代码
├── config.py           # 配置管理
├── requirements.txt    # 依赖包
├── config.json        # 配置文件
├── data/              # 数据输出目录
└── browser_data/      # 浏览器数据目录
```

## 🔧 技术特点

- **基于 Playwright**: 使用现代浏览器自动化框架
- **异步处理**: 提高爬取效率
- **模块化设计**: 易于扩展和维护
- **配置灵活**: 支持配置文件和命令行参数
- **数据存储**: 支持 JSON、CSV、SQLite 格式

## 📊 数据格式

### 小红书数据示例
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

### 抖音数据示例
```json
{
  "platform": "douyin",
  "keyword": "技术",
  "title": "前端开发技巧分享",
  "author": "技术达人",
  "link": "https://www.douyin.com/...",
  "likes": "5678",
  "crawl_time": "2024-01-01T12:00:00"
}
```

## ⚠️ 重要提醒

- 本项目仅供**学习和研究**使用
- 请遵守目标平台的robots.txt规则
- 合理控制请求频率，避免对平台造成负担
- 不得用于商业用途或非法用途
- 使用前请仔细阅读相关法律法规

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

感谢以下开源项目的支持：
- [Playwright](https://playwright.dev/)
- [aiofiles](https://github.com/Tinche/aiofiles)

---

**免责声明**: 本项目仅供学习和研究使用，使用者应自行承担使用风险。 