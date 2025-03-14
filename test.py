import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from pandas import Series,DataFrame

def test():
    #单层索引
    sa = pd.Series([1, 2, 3], index=list('abc'))
    print(sa)


def draw_histogram():
    

def draw_curve():
    # 计算正弦曲线上点的 x 和 y 坐标
    x = np.arange(0,  3  * np.pi,  0.1) 
    y = np.sin(x)
    plt.title("sine wave form")

    # 使用 matplotlib 来绘制点
    plt.plot(x, y) 
    plt.show()

def main():
    #draw_curve()
    test()
    return

if __name__ == '__main__':
    main()






