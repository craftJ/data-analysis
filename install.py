# 安装依赖库

import subprocess
import sys

def install_check():
    #TODO: 需要自动实现更新环境到符合要求
    print("Python Version:",sys.version)
    subprocess.check_call([sys.executable, "-m", "pip","-V"])
    return

def install_packages():
    packages = [
        "numpy",
        "matplotlib",
        "scipy",
        "pandas",
        "plotly",
        "seaborn",
        "pynimate"
    ]
    print("Python libs are installing...")
    for package in packages:
        subprocess.check_call([sys.executable,
        "-m", "pip", "install", package, "-i", 
        "https://pypi.tuna.tsinghua.edu.cn/simple"])
    print("Install Finished！")

if __name__ == "__main__":
    install_check()
    install_packages()



