# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。

import os
import sys
import subprocess
import platform

# 检查是否安装了必要的依赖
def check_dependencies():
    required_packages = ['flask', 'playwright', 'httpx']
    missing_packages = []

    try:
        import pkg_resources
        for package in required_packages:
            try:
                pkg_resources.get_distribution(package)
            except pkg_resources.DistributionNotFound:
                missing_packages.append(package)
    except ImportError:
        print('无法检查依赖项，请确保已安装所有必要的包。')
        return False

    if missing_packages:
        print(f'缺少必要的依赖包: {missing_packages}')