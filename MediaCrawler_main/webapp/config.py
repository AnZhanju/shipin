# Web应用配置文件

# 应用端口
PORT = 5000

# 调试模式
DEBUG = True

# 爬取配置
CRAWLER_CONFIG = {
    # 爬取超时时间(秒)
    'TIMEOUT': 30,
    # 最大并发数
    'MAX_CONCURRENCY': 5,
    # 是否启用IP代理
    'ENABLE_IP_PROXY': False,
    # IP代理池数量
    'IP_PROXY_POOL_COUNT': 5,
}

# 存储配置
STORAGE_CONFIG = {
    # 下载文件保存路径
    'DOWNLOAD_FOLDER': 'downloads',
    # 最大文件大小限制(MB)
    'MAX_FILE_SIZE': 100,
}

# 日志配置
LOGGING_CONFIG = {
    'LEVEL': 'INFO',
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'FILE': 'webapp.log',
}