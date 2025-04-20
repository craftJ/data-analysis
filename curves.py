# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt

def func_power(x,a):
    return x ** a

#设置绘图风格,设置支持中文
def set_style_and_chinese(plt):
    #显示所有支持的style
    #print(plt.style.available)
    plt.style.use('seaborn-v0_8-pastel')
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    return

#正弦函数
def draw_curve_sin():
    # 计算正弦曲线上点的 x 和 y 坐标
    x = np.arange(0,  4 * np.pi,  0.1) 
    y = np.sin(x)
    set_style_and_chinese(plt)
    plt.title("正弦函数 - y=sin(x)")
    plt.plot(x, y) 
    plt.show()
    return

#余弦函数
def draw_curve_cos():
    # 计算正弦曲线上点的 x 和 y 坐标
    x = np.arange(0,  4 * np.pi,  0.1) 
    y = np.cos(x)
    set_style_and_chinese(plt)
    plt.title("余弦函数 - y=cos(x)")
    plt.plot(x, y) 
    plt.show()
    return

#螺旋线
def draw_curve_helix():
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
    set_style_and_chinese(plt)
    plt.title("螺旋线函数(helix)")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    return

#自定义函数
def draw_curve_custom():
    x = np.linspace(0, 1000000, 100)
    y = func_power((x-2), 3)*(x+1)
    plt.title("自定义函数 - y=(x-2)^3 * (x+1)")
    plt.plot(x, y) 
    plt.show()
    return

def main():
    draw_curve_sin()
    draw_curve_cos()
    draw_curve_helix()
    draw_curve_custom()
    return

if __name__ == '__main__':
    main()
