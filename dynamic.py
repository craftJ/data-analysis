import numpy as np 
import matplotlib.pyplot as plt
import os
import random
from scipy.interpolate import interp1d
from matplotlib.animation import FuncAnimation
import pandas as pd
from pandas import Series,DataFrame
import plotly.express as px
import plotly.graph_objects as go

#pynimate 要求 Python 版本至少为 3.9
import pynimate as nim

#用于调试
from debug import dbg_info as dbg

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
                            frames=len(time_dense), init_func=init, blit=True, interval=50)
                            #frames=len(time_dense), init_func=init, blit=True)
        # 显示动画
        plt.show()
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
        plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
        plt.rcParams['axes.unicode_minus'] = False

        # 读取数据
        dataset= os.path.join('./dataset/searborn-data/', 'healthexp.csv')
        dbg("info",1,dataset)
        df_data = pd.read_csv(dataset, encoding='utf-8', header=None, 
                    names=['year', 'country', 'Spending_USD','Life_Expectancy']).set_index("year")
        # pivot_table即类似Excel的数据透视图
        df = pd.pivot_table(df_data, values='Life_Expectancy', 
            index=['year'], columns=['country'], fill_value=0).head(200)

        # 新建画布
        cnv = nim.Canvas(figsize=(12.8, 7.2), facecolor="#001219")
        bar = nim.Barplot(
            df, "%Y/%m/%d", "2h", post_update=None, rounded_edges=True, grid=False, n_bars=10
        )
        bar.set_title("动态排名图", color="w", weight=600, x=0.15, size=30)
        bar.set_time(
            callback=lambda i, datafier: datafier.data.index[i].strftime("%Y-%m-%d"), color="w", y=0.2, size=20
        )
        bar.set_bar_annots(color="w", size=13)
        bar.set_xticks(colors="w", length=0, labelsize=13)
        bar.set_yticks(colors="w", labelsize=13)
        cnv.add_plot(bar)
        cnv.animate()
        cnv.save("dynamic_ranking", 24, "gif")  # 保存为 GIF
    elif mode == 2:
        dbg("info",0,"unkown mode!!!")
    elif mode == 3:
        dbg("info",0,"unkown mode!!!")
    else:
        dbg("info",0,"unkown mode!!!")
    return




def main():
    #draw_dynamic_linechart()
    draw_dynamic_rankbar()
    return

if __name__ == '__main__':
    main()

