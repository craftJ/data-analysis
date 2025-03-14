import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from pandas import Series,DataFrame

def test():
    #单层索引
    sa = pd.Series([1, 2, 3], index=list('abc'))
    print(sa)


#直方图
def draw_histogram():
    fig,axes = plt.subplots(2,1)
    data = pd.Series(np.random.randn(17),index=list('abcdefghijklmnopq'))
    data.plot(kind='bar',ax=axes[0],color='k',alpha=0.7)
    data.plot(kind='barh',ax=axes[1],color='k',alpha=0.7)
    plt.show()
    return

#函数曲线
def draw_curve():
    # 计算正弦曲线上点的 x 和 y 坐标
    x = np.arange(0,  3  * np.pi,  0.1) 
    y = np.sin(x)
    plt.title("y=sin(x)")
    plt.plot(x, y) 
    plt.show()

def main():
    #draw_curve()
    draw_histogram()
    #test()
    return

if __name__ == '__main__':
    main()







