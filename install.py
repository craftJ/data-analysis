# -*- coding: utf-8 -*-
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
        #科学运算
        "scipy",
        "pandas",
        #交互式图标
        "plotly",
        #地图
        "geopandas",
        #图表,绘图
        "seaborn",
        #动画，动态图
        "pynimate",
        #Echarts类图表绘制
        "pyecharts",
        #韦恩图
        "matplotlib_venn",
        #多集合关联图
        "upsetplot",
        #用于生成词云图
        "wordcloud",
        #图像处理库，提供了广泛的图像处理功能，包括图像的打开、保存、裁剪、旋转、过滤等
        "Pillow",
        #用于创建、操作和研究复杂网络的结构、动态和功能。它提供了丰富的功能，可以处理各种类型的图（如无向图、有向图、加权图等
        "networkx",
        "squarify"
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



