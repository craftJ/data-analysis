# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt
import os
import random
from scipy.interpolate import interp1d
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
import pandas as pd
from pandas import Series,DataFrame
import plotly.express as px
import plotly.graph_objects as go

#pynimate 要求 Python 版本至少为 3.9
import pynimate as nim

#用于调试
import debug as dbg


#设置绘图风格,设置支持中文
def set_style_and_chinese(plt):
    #显示所有支持的style
    #print(plt.style.available)
    plt.style.use('seaborn-v0_8-pastel')
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    return


#动态折线图
def draw_dynamic_linechart(): 
    mode = 1
    if mode == 1:
        # 固定随机数种子，保证每次随机一样
        np.random.seed(0)
        time = np.arange(0, 100, 1)  # 时间范围
        data = np.random.randn(len(time)).cumsum()  # 随机生成的累积和数据
        # 使用插值生成更密集的数据点
        # 当 kind='cubic' 时，interp1d 会生成一个三次插值函数。三次插值是一种平滑的插值方法，通过拟合三次多项式来生成数据点之间的值，使得生成的曲线更加平滑
        f = interp1d(time, data, kind='cubic')
        time_dense = np.linspace(0, len(time) - 1, 500)  # 更密集的时间点
        data_dense = f(time_dense)  # 插值后的数据
        # 创建一个图形和轴
        fig, ax = plt.subplots()
        line, = ax.plot([], [], lw=2)  # 创建一个空的折线图
        ax.set_xlim(0, len(time))  # 设置 x 轴范围
        ax.set_ylim(min(data_dense), max(data_dense))  # 设置 y 轴范围

        # 初始化函数
        def init():
            line.set_data([], [])
            return line,

        # 更新函数
        def update(frame):
            line.set_data(time_dense[:frame], data_dense[:frame])  # 更新数据
            return line,

        # 创建动画,interval调整帧间隔ms，以调整显示速度
        ani = FuncAnimation(fig, update, 
                            frames=len(time_dense), init_func=init, blit=True, interval=5)
                            #frames=len(time_dense), init_func=init, blit=True)
        # 显示动画
        set_style_and_chinese(plt)
        plt.title("动态折线图",fontsize=16)
        plt.show()
        #ani.save('./docs/dynamicLine.gif', writer='pillow', fps=10)
    elif mode == 2:
        # 生成示例数据
        np.random.seed(0)
        time = np.arange(0, 100, 1)  # 时间范围
        data = np.random.randn(len(time)).cumsum()  # 随机生成的累积和数据
        # 创建动态折线图
        fig = go.Figure(data=go.Scatter(
            x=time,
            y=data,
            mode='lines',
            line=dict(shape='spline'),  # 使用平滑曲线
            line_color='rgba(31, 119, 180, 0.8)',
            line_width=2
        ))
        # 添加动态效果
        fig.update_layout(
            title='动态折线图',
            xaxis_title='时间',
            yaxis_title='值',
            template='plotly_dark'
        )
        # 显示图表
        fig.show()
    return

#动态排名图
def draw_dynamic_rankbar():
    mode = 1
    if mode == 1:
        # 中文显示
        #plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
        #plt.rcParams['axes.unicode_minus'] = False
        dbg.dbg_pwd()
        # 读取数据
        datapath = r'./dataset/tiger-data'
        dataset= os.path.join(datapath, 'gdp.csv')
        dbg.dbg_info("info",1,dataset)
        df_data = pd.read_csv(dataset, encoding='utf-8',
                    #skiprows=range(1, 5), 
                    nrows=11,
                    usecols=["Country Name","1960","1961","1962","1963","1964","1965","1966","1967",
                             "1968","1969","1970","1971","1972","1973","1974","1975","1976","1977",
                             "1978","1979","1980","1981","1982","1983","1984","1985","1986","1987",
                             "1988","1989","1990","1991","1992","1993","1994","1995","1996","1997",
                             "1998","1999","2000","2001","2002","2003","2004","2005","2006","2007",
                             "2008","2009","2010","2011","2012","2013","2014","2015","2016","2017",
                             "2018","2019","2020","2021","2022","2023"], header=0)

        print("\n\n",df_data,"\n\n")

        # 转换宽表为长表（年份从列变为行）
        df_long = df_data.melt(
            id_vars="Country Name",     # 保持不变的列（标识符）
            var_name="Year",       # 新列名（原列名转为行）
            value_name="GDP"     # 新列名（原数值）
            )
        print("\n\n",df_long,"\n\n")

        # pivot_table即类似Excel的数据透视图
        # 关键的4个字段 index
        # 1. index：Index就是层次字段，要通过透视表获取什么信息就按照相应的顺序设置字段
        # 2. values：关注的数据
        # 3. Aggfunc: 设置我们对数据聚合时进行的函数操作
        # 4. Columns类似Index可以设置列层次字段，它不是一个必要参数，作为一种分割数据的可选方式
        #year,month,passengers
        df = pd.pivot_table(df_long, values='GDP', 
                index=['Year'], columns=['Country Name'], fill_value=0)

        print("\n\n",df,"\n\n")

        # 新建画布
        cnv = nim.Canvas(figsize=(12.8, 7.2), facecolor="white")
        bar = nim.Barplot(
            df, "%Y", "1YE", post_update=None, rounded_edges=False, grid=True, n_bars=20
        )
        bar.set_title("动态排名图 - Countries' GDP Rank", color="black",x=0.3,weight=500,size=20)
        bar.set_time(
            callback=lambda i, datafier: datafier.data.index[i].strftime("%Y"), 
            color="w", y=0.2, size=20
        )
        # 生成默认颜色列表
        default_colors = cm.viridis(np.linspace(0, 1, len(df.columns)))
        # 定义特定条形的颜色
        custom_colors = {
            "China": "#E4080A"
        }
        # 替换特定条形的颜色
        colors = [custom_colors.get(col, default) for col, default in 
            zip(df.columns, default_colors)]
        # 设置条形图颜色
        bar.set_bar_color(colors)

        bar.set_bar_annots(color="black", size=13)
        bar.set_xticks(colors="black", length=0, labelsize=13)
        bar.set_yticks(colors="black", labelsize=13)
        cnv.add_plot(bar)
        cnv.animate(interval = 100)
        plt.show()
        # 保存为 GIF
        #cnv.save("./docs/Country-GDP-Rank", 300, "gif") 
    elif mode == 2:
        dbg.dbg_info("info",0,"unkown mode!!!")
    elif mode == 3:
        dbg.dbg_info("info",0,"unkown mode!!!")
    else:
        dbg.dbg_info("info",0,"unkown mode!!!")
    return


def main():
    draw_dynamic_linechart()
    draw_dynamic_rankbar()
    return

if __name__ == '__main__':
    main()

