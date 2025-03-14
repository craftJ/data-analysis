import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from pandas import Series,DataFrame
import inspect
import sys

def dbg_caller():
    # 获取调用者的帧信息
    frame = sys._getframe(1)  # 1 表示调用栈的上一层
    caller_line_number = frame.f_lineno
    caller_function_name = frame.f_code.co_name
    print(f"func:{caller_function_name}, line:{caller_line_number}")
    return

def test():
    #单层索引
    sa = pd.Series([1, 2, 3], index=list('abc'))
    print(sa)

def show(plt,secs):
    plt.show(block=False)
    plt.pause(secs)
    plt.close()
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
def draw_curve():
    # 计算正弦曲线上点的 x 和 y 坐标
    x = np.arange(0,  3  * np.pi,  0.1) 
    y = np.sin(x)
    plt.title("y=sin(x)")
    plt.plot(x, y) 
    show(plt, 1)
    return

def main():
    #draw_curve()
    draw_histogram()
    draw_hist()
    draw_bar()
    #test()
    return

if __name__ == '__main__':
    main()







