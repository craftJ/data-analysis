# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt

def func_power(x,a):
    return x ** a

#函数曲线
def draw_curve(funtype):
    if funtype == "sin":
        # 计算正弦曲线上点的 x 和 y 坐标
        x = np.arange(0,  4 * np.pi,  0.1) 
        y = np.sin(x)
        plt.title("y=sin(x)")
        plt.plot(x, y) 
        plt.show()
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
        plt.show()
    else:  
        x = np.linspace(0, 1000000, 100)
        y = func_power((x-2), 3)*(x+1)
        plt.title("y=(x-2)^3 * (x+1)")
        plt.plot(x, y) 
        plt.show()
    return

def main():
    draw_curve("")
    return

if __name__ == '__main__':
    main()
