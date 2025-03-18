import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from pandas import Series,DataFrame
import inspect
import sys
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm

def dbg_caller():
    # 获取调用者的帧信息
    frame = sys._getframe(1)  # 1 表示调用栈的上一层
    caller_line_number = frame.f_lineno
    caller_function_name = frame.f_code.co_name
    print(f"func:{caller_function_name}, line:{caller_line_number}")
    return

def show(plt,secs=None):
    if secs is not None:
        plt.show(block=False)
        plt.pause(secs)
        plt.close()
    else:
        plt.show()
    return

#箱线图
def draw_boxplot():
    x = np.random.randn(1000)
    y = np.random.randn(500)
    z = np.random.randn(1500)
    plt.boxplot((x, y, z), labels=('x', 'y', 'z'),patch_artist=True,showmeans=True,)
    show(plt)
    return

#热力图
def draw_heatmap():
    arry_size = 20
    # 自定义数据及坐标轴
    values = np.random.uniform(0, 1000, size=(arry_size, arry_size))

    # 使用列表推导式生成x轴和y轴的定义
    x_prefix = "name-"
    y_prefix = "vaule-"
    x_ticks = [f"{x_prefix}{i+1}" for i in range(arry_size)]
    y_ticks = [f"{y_prefix}{i+1}" for i in range(arry_size)]
    
    # 绘制热力图，设置标题及坐标名称
    #viridis：从深蓝到黄绿色的渐变。
    #plasma：从深红到黄色的渐变。
    #inferno：从黑色到红色的渐变。
    #magma：从黑色到橙色的渐变。
    #cividis：从深蓝到黄色的渐变。
    #coolwarm：从蓝色到红色的渐变，中间为白色。
    #RdBu：从红色到蓝色的渐变。
    #Blues：从浅蓝到深蓝的渐变。
    #Reds：从浅红到深红的渐变
    #_r后缀:表示颜色和值反向映射
    ax = sns.heatmap(values, xticklabels=x_ticks, yticklabels=y_ticks, cmap="Blues")
    ax.set_title('Heatmap') 
    ax.set_xlabel('x label') 
    ax.set_ylabel('y label')
    show(plt,2)
    return

#直方图
def draw_histogram():
    fig,axes = plt.subplots(2,1)
    data = pd.Series(np.random.randn(17),index=list('abcdefghijklmnopq'))
    data.plot(kind='bar',ax=axes[0],color='red',alpha=0.7)
    data.plot(kind='barh',ax=axes[1],color='blue',alpha=0.7)
    show(plt,1)
    return

#直方图
def draw_hist():
    data = np.random.randn(1000)  # 生成随机数据
    plt.hist(data, bins=30, color='blue', alpha=0.7)
    plt.title("Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    show(plt,1)
    return

#柱状图
def draw_bar():
    categories = ['A', 'B', 'C', 'D']
    values = [10, 15, 7, 5]
    plt.bar(categories, values, color='green', alpha=0.7)
    plt.title("Bar Chart")
    plt.xlabel("Category")
    plt.ylabel("Value")
    show(plt,1)
    return

#函数曲线
def draw_curve(funtype):
    if funtype == "sin":
        # 计算正弦曲线上点的 x 和 y 坐标
        x = np.arange(0,  4 * np.pi,  0.1) 
        y = np.sin(x)
        plt.title("y=sin(x)")
        plt.plot(x, y) 
        show(plt, 1)
    elif funtype == "helix":
        # 定义参数
        a = 1  # 半径
        b = 0.2  # 螺距
        t = np.linspace(0, 8 * np.pi, 100)  # 参数 t 的取值范围

        # 计算螺旋线的坐标
        x = a * np.cos(t)
        y = a * np.sin(t)
        z = b * t

        # 绘制螺旋线
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111,projection='3d')
        ax.plot(x, y, z)

        # 设置坐标轴标签
        plt.title("helix")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        show(plt)
    else:
        print("Unknown function!!")
    return

#Kernel Density Estimation
def draw_kde():
    #随机样本点
    dataset = np.array([10,2,-2,22,1,3,6,19,7,3,16,5,12,0])
    fig, ax = plt.subplots(figsize=(10, 4))
    #绘制kde
    sns.kdeplot(ax=ax, data=dataset, bw_adjust=0.3)
    #标注样本点位置及注解
    ax.plot(dataset, np.zeros_like(dataset)+0.05, 's', markersize=8, color='black')
    for index, x in enumerate(dataset):
        ax.annotate(r'$x_{}$'.format(index + 1), xy=[x, 0.04], horizontalalignment='center', fontsize=12)
    plt.show()
    return

def main():
    #draw_curve("helix")
    #draw_histogram()
    #draw_hist()
    #draw_bar()
    #draw_heatmap()
    #draw_boxplot()
    draw_kde()
    return

if __name__ == '__main__':
    main()







