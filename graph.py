# -*- coding: utf-8 -*-
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
from matplotlib.animation import FuncAnimation
import pandas as pd
from pandas import Series,DataFrame
import inspect
import sys
import seaborn as sns
import os
import random
from scipy.interpolate import interp1d
from scipy.stats import norm
# 用plotly是交互式的sankey图,web端弹出页面后可以交互显示数据详细信息,plotly很强大,交互式的地图,还可以伸缩,旋转！！
import plotly.express as px
import plotly.graph_objects as go

# mpl_toolkits 并不是一个独立的 Python 包,而是 matplotlib 库
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#for 地理相关绘图
import geopandas as gpd
from shapely.geometry import Point
from pyecharts import options as opts
from pyecharts.charts import Map 
from shapely.geometry import Point
#for venn图
from matplotlib_venn import venn3
from upsetplot import plot as upset_plot
from upsetplot.data import from_contents
from upsetplot import generate_counts
#for 词云图
from wordcloud import WordCloud
#for 图片处理
from PIL import Image
#for Voronoi图
from scipy.spatial import Voronoi, voronoi_plot_2d
#for Funnel图
from pyecharts.charts import Funnel
from pyecharts.faker import Faker
#图结构处理
import networkx as nx
import squarify
import string

#调试
import debug as dbg


def show(plt,secs=None):
    if secs is not None:
        plt.show(block=False)
        plt.pause(secs)
        plt.close()
    else:
        plt.show()
    return

#设置绘图风格,设置支持中文
def set_style_and_chinese(plt):
    #显示所有支持的style
    #print(plt.style.available)
    plt.style.use('seaborn-v0_8-pastel')
    plt.rcParams['font.sans-serif'] = ['FangSong']
    plt.rcParams['axes.unicode_minus'] = False
    return

#本地数据集加载
def load_dataset(name):
    local_seaborn = r"./dataset/seaborn-data"
    local_tiger = r"./dataset/tiger-data"
    dataFrame = None
    if name == 'iris':
        # === 1. 加载本地数据集 ===
        try:
            # 从当前目录读取CSV文件(根据实际路径调整)
            dataset = os.path.join(local_seaborn, 'iris.csv')
            iris_df = pd.read_csv(dataset)
            # 检查数据是否加载成功
            if iris_df.empty:
                raise FileNotFoundError("文件为空或格式不正确")
            iris_df['species'] = iris_df['species'].astype(str)
            print("数据加载成功！前5行示例：")
            print(iris_df.head())
        except FileNotFoundError:
            # 如果文件不存在,从网络加载备用数据
            print("本地文件未找到,改用sklearn内置数据集")
            from sklearn.datasets import load_iris
            iris = load_iris()
            iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
            iris_df['species'] = [iris.target_names[i] for i in iris.target]

        # === 2. 数据预处理 ===
        # 统一列名格式(如果本地文件列名不同)
        iris_df.columns = iris_df.columns.str.lower().str.replace(' ', '_')
        dataFrame = iris_df
        print("\n可用特征列：", iris_df.columns.tolist())

    elif name == 'shopping':
        file_path = os.path.join(local_tiger, 'online-shopping.xlsx')
        dataFrame = pd.read_excel(file_path)

    elif name == 'penguins':
        dataset = os.path.join(local_seaborn, 'penguins.csv')
        dataFrame = pd.read_csv(dataset)

    else:
        dbg.dbg_info('err',1,"unknown dataset name!!\n")

    return dataFrame


#柱状图
#多用于多类数据数值比较
def draw_bar():
    fig,axes = plt.subplots(2,1)
    data = pd.Series(np.random.randn(17),index=list('abcdefghijklmnopq'))
    data.plot(kind='bar',ax=axes[0],color='red',alpha=0.7)
    data.plot(kind='barh',ax=axes[1],color='blue',alpha=0.7)

    #设置绘图风格,支持中文
    set_style_and_chinese(plt)

    axes[0].set_title('垂直柱状图(Vertical Bar Chart)')  # 设置标题
    axes[0].set_xlabel('Categories')         # 设置x轴标签
    axes[0].set_ylabel('Values')             # 设置y轴标签

    axes[1].set_title('水平柱状图(Horizontal Bar Chart)')  # 设置标题
    axes[1].set_xlabel('Values')               # 设置x轴标签
    axes[1].set_ylabel('Categories')           # 设置y轴标签

    # 调整子图间距防止标签重叠
    plt.tight_layout()

    show(plt)

    return

#直方图
#用于同类数据看分布
def draw_histogram():
    # 生成随机数据
    data = np.random.randn(1000)  

    #counts 是一个数组,表示每个直方图柱子(bin)的高度
    #bins 是一个数组,表示直方图的边界
    #patches 是一个包含 matplotlib.patches.Rectangle 对象的列表,每个 Rectangle 对应一个柱子。这些对象可以用于进一步自定义柱子的外观,例如设置颜色、边框等
    counts,bins,patchs = plt.hist(data, bins=30, color='blue',edgecolor='white', alpha=0.7)
    # 添加数值标签
    for count, bin in zip(counts, bins):
        plt.text(bin + (bins[1] - bins[0])/2, count, str(int(count)), ha='center', va='bottom')

    #设置绘图风格,支持中文
    set_style_and_chinese(plt)

    plt.title("直方图(Histogram)")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    show(plt)
    return

#热力图
def draw_heatmap():
    arry_size = 20
    # 自定义数据及坐标轴
    values = np.random.uniform(0, 1000, size=(arry_size, arry_size))

    # 使用列表推导式生成x轴和y轴的定义
    x_prefix = "City-"
    y_prefix = "vaule-"
    x_ticks = [f"{x_prefix}{i+1}" for i in range(arry_size)]
    y_ticks = [f"{y_prefix}{i+1}" for i in range(arry_size)]
    
    # 绘制热力图,设置标题及坐标名称
    #viridis:从深蓝到黄绿色的渐变。
    #plasma:从深红到黄色的渐变。
    #inferno:从黑色到红色的渐变。
    #magma:从黑色到橙色的渐变。
    #cividis:从深蓝到黄色的渐变。
    #coolwarm:从蓝色到红色的渐变,中间为白色。
    #RdBu:从红色到蓝色的渐变。
    #Blues:从浅蓝到深蓝的渐变。
    #Reds:从浅红到深红的渐变
    #_r后缀:表示颜色和值反向映射
    ax = sns.heatmap(values, xticklabels=x_ticks, yticklabels=y_ticks, cmap="Blues")

    #设置绘图风格,支持中文
    set_style_and_chinese(plt)
    ax.set_title('热力图(Heatmap)') 
    ax.set_xlabel('Location') 
    ax.set_ylabel('Population density')
    show(plt)
    return


#箱线图
def draw_boxplot():
    #随机生成不同月份的销售数据
    df = pd.DataFrame({
        'Jan': np.random.normal(100, 20, 50),
        'Feb': np.random.normal(120, 25, 50),
        'Mar': np.random.normal(90, 15, 50)
    })

    sns.boxplot(df)
    set_style_and_chinese(plt)
    plt.title("箱线图(Box Plot)")
    plt.xlabel("Months")
    plt.ylabel("SalesCount")
    plt.show()
    return

#Kernel Density Estimation
def draw_kde():
    #采用iris数据集
    dataset = load_dataset('iris')

    plt.figure(figsize=(10, 6))
    sns.kdeplot(
        data=dataset,
        x='petal_length',
        hue='species',
        fill=True,
        legend=True,
        alpha=0.3,
        palette='viridis',
        bw_adjust=0.8  # 带宽调整
    )
    set_style_and_chinese(plt)
    plt.title('概率密度图(KDE plot) - 花瓣长度概率密度分布', fontsize=14)
    plt.xlabel('花瓣长度 (cm)')
    plt.ylabel('概率密度')
    #这里需要手动添加图例,按照图显顺序应该是['setosa','versicolor','virginica'],但如此传入后图例是相反的
    plt.legend(title='物种',labels=['virginica','versicolor','setosa'])
    plt.show()
    return

#小提琴图
def draw_violinplot():
    #原始数据读取
    data_read = load_dataset('shopping')

    #坐标轴负号的处理
    plt.rcParams['axes.unicode_minus']=False
    # 绘制分组小提琴图
    sns.violinplot(
                x = "website store", # 指定x轴的数据
                #x = 'name',
                y = "total amount", # 指定y轴的数据
                hue = "sex", # 指定分组变量
                data = data_read, # 指定绘图的数据集
                #order = ['7','8','9','10','11','12'], # 指定x轴刻度标签的顺序
                order = ['pdd','jingdong','taobao'],
                #order = ['lisa','joe','tom','jerry','james'],
                density_norm='count',#
                split = True, # 将小提琴图从中间割裂开,形成不同的密度曲线；
                palette = 'RdBu' # 指定不同性别对应的颜色(因为hue参数为设置为性别变量)
                )
    #设置绘图风格,支持中文
    set_style_and_chinese(plt)
    # 添加图形标题
    plt.title('小提琴图(violin plot): 每月消费情况')
    # 设置图例
    plt.legend(loc = 'upper left', ncol = 2)
    # 显示图形
    plt.show()
    return

#散点矩阵图
def draw_scatter_matrix(): 
    # 创建示例数据
    if 0:
        data = {
            'A': [10, 5, 8, 7, 2,15,11,9,13,1],
            'B': [5, 4, 3, 2, 1,2,3,4,5,7],
            'C': [2, 3, 4, 5, 6,3,4,5,6,7],
            'D': [6, 2, 4, 3, 2,3,2,1,4,6],
            'species': ["a","b","c","c","b","a","a","c","b","b"]
        }
        df = pd.DataFrame(data)
        print(df)
    else:
        #采用本地seaborn数据集
        df = load_dataset('penguins')
        df = df.iloc[:,0:4]
        print(df)

    if 1:
        # 使用 seaborn 绘制散点矩阵图,对角线显示核密度估计
        #kind:用于控制非对角线上的图的类型,可选"scatter"与"reg",对应散点,拟合回归线
        #diag_kind:控制对角线上的图的类型,可选"hist"与"kde",对应直方图,概率密度估计
        '''
        sns.pairplot(df, diag_kind='kde',kind='reg')
        sns.pairplot(df, diag_kind='kde',kind='scatter')
        sns.pairplot(df, diag_kind='hist',kind='reg')
        '''
        g = sns.pairplot(df, diag_kind='hist',kind='scatter',hue="species")

        #设置绘图风格,支持中文
        set_style_and_chinese(plt)
        # 调整整体图形布局
        g.figure.set_size_inches(10, 9)  # 设置整个图形对象的尺寸
        g.figure.suptitle("散点矩阵图(scatter matrix):企鹅喙特征分析", y=0.95, fontsize=16) 
        # 关键调整：增加顶部边距
        plt.subplots_adjust(top=0.9)  # 保留10%的顶部空间
        show(plt)
    else:
        # 使用 pandas 绘制散点矩阵图作为比较,
        # 跟想象的不一样,不同的库绘制出来的视觉效果还是比较大的,
        # 并且这里的直方图同seaborn的有较大差异
        '''
        pd.plotting.scatter_matrix(df, diagonal='kde')
        '''
        pd.plotting.scatter_matrix(df, diagonal='hist')
        show(plt)
    return

#六边形箱图
def draw_hexbin():
    df = pd.DataFrame(np.random.randn(1000, 2), columns=['a', 'b'])
    df['b'] = df['b'] + np.arange(1000)
    df.plot.hexbin(x='a', y='b', gridsize=25)

    #设置绘图风格,支持中文
    set_style_and_chinese(plt)
    # 添加标题和坐标轴说明
    plt.title('六边形箱图(Hex bin)', fontsize=16)  # 添加标题
    plt.xlabel('city', fontsize=12)  # 添加 x 轴说明
    plt.ylabel('degree', fontsize=12)  # 添加 y 轴说明

    show(plt)
    return

#简单饼图
def draw_pie():
    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect="equal"))
    recipe = ["375 g flour",
            "75 g sugar",
            "250 g butter",
            "300 g berries",
            "200 g milk"]
    data = [float(x.split()[0]) for x in recipe]
    ingredients = [x.split()[-1] for x in recipe]
    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d} g)"
    
     # 自定义颜色
    colors = ['#cc6666', '#3377cc', '#66cc66', '#cc9966',"#aa2233"]
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                    colors = colors,
                                    textprops=dict(color="w"))
    ax.legend(wedges, ingredients,
            title="Ingredients",
            loc="center left",
            #bbox_to_anchor 的参数可以是一个元组 (x, y) 或 (x, y, width, height)。
            # 具体含义如下：
            #(x, y)：指定锚点的坐标,相对于 loc 参数指定的位置。
            #(x, y, width, height)：指定锚点的坐标以及边界框的宽度和高度。
            bbox_to_anchor=(0.95, 0, 0.5, 1))

    #设置绘图风格,支持中文
    set_style_and_chinese(plt)
    # 添加标题和坐标轴说明
    plt.setp(autotexts, size=10, weight="bold")
    plt.title('简单饼图(Pie)-烘培食物占比', fontsize=16)
    plt.show()
    return


#嵌套饼图
def draw_multipie():
    #mode == 1：嵌套饼图(使用bar,极坐标系方式绘制叠加)
    #mode == 2：嵌套饼图(使用pie绘制叠加)
    mode = 1
    if mode == 1:
        import matplotlib.pyplot as plt
        import numpy as np
        #嵌套饼图采用polar极坐标系
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection="polar"))
        size = 0.3
        vals = np.array([[60., 32.,10.], [37., 40.,33.], [29., 10.,54.]])
        print(vals,"\n")    
        # 数值归一化为弧度
        valsnorm = vals/np.sum(vals)*2*np.pi
        print(valsnorm,"\n")
        # Obtain the ordinates of the bar edges
        # 在极坐标系下,条形图的“ordinates”(纵坐标)实际上是指条形的半径边界值。
        # 注意！！这里使用flatten转换后再cumsum不断累加,达到了不同分类占用弧度的不断累加,方便得到每个大类的开始弧度位置
        valsleft = np.cumsum(np.append(0, valsnorm.flatten()[:-1])).reshape(vals.shape)
        print(valsleft,"\n")

        #饼图颜色映射
        cmap = plt.colormaps["tab20c"]
        #大类颜色,0,4,8
        outer_colors = cmap(np.arange(3)*4)
        #子类颜色,分布在大类区间范围,可以使同类色系一致
        inner_colors = cmap([1, 2, 3, 5, 6, 7, 9, 10,11])
        
        #极坐标/直角坐标系情况下,参数含义分别如下:
        #x:条形图的起始角度(以弧度为单位)  / X轴起始位置
        #width:条形图的宽度(以弧度为单位) / 条形图宽度
        #bottom:条形图的起始半径。         / 条形图底部位置
        #height:条形图的高度(即半径的增量)/ 条形图高度
        #color:条形图的填充颜色 / 同
        #edgecolor:条形图边框的颜色 /同
        #linewidth:条形图边框的宽度/ 同
        #align:条形图的对齐方式。/同
        # 取valsleft第一列,绘制最外圈的大分类,宽度为valsnorm中每行相加,实际就是子类的弧度相加
        ax.bar(x=valsleft[:, 0],
            width=valsnorm.sum(axis=1), bottom=1-size, height=size,
            color=outer_colors, edgecolor='w', linewidth=1, align="edge")

        # 添加标注信息
        for i, (left, width) in enumerate(zip(valsleft[:, 0], valsnorm.sum(axis=1))):
            # 计算标注的位置
            x = left + width / 2  # 标注的 x 坐标(条形的中心)
            y = 1 - size / 2  # 标注的 y 坐标(条形的中心)
            # 添加标注
            ax.annotate(f"{width:.2f}",  # 标注文本
                        xy=(x, y),  # 标注的位置
                        xytext=(0, 5),  # 文本的偏移量(相对于标注位置)
                        textcoords="offset points",  # 文本的坐标系统
                        ha='center',  # 水平对齐方式
                        va='bottom',  # 垂直对齐方式
                        fontsize=12,  # 字体大小
                        color='white')  # 字体颜色

        # 取valsleft所有元素,按照行优先二维转一维,绘制所有子类占比,宽度为子类各自的归一化弧度
        ax.bar(x=valsleft.flatten(),
            width=valsnorm.flatten(), bottom=1-2*size, height=size,
            color=inner_colors, edgecolor='w', linewidth=1, align="edge")

        # 添加标注信息
        for i, (left, width) in enumerate(zip(valsleft.flatten(), valsnorm.flatten())):
            # 计算标注的位置
            x = left + width / 2  # 标注的 x 坐标(条形的中心)
            y = 1 - 2 * size + size / 2  # 标注的 y 坐标(条形的中心)
            # 添加标注
            ax.annotate(f"{width:.2f}",  # 标注文本
                        xy=(x, y),  # 标注的位置
                        xytext=(0.1, 0.1),  # 文本的偏移量(相对于标注位置)
                        textcoords="offset points",  # 文本的坐标系统
                        ha='center',  # 水平对齐方式
                        va='bottom',  # 垂直对齐方式
                        fontsize=12,  # 字体大小
                        color='white')  # 字体颜色

        #设置绘图风格,支持中文
        set_style_and_chinese(plt)
        #关闭当前坐标轴(axes)的所有轴线(包括刻度、标签和边框)
        ax.set_axis_off()
        plt.title("嵌套饼图(nested pie) - 销售数据", fontsize=16)  # 添加标题
        plt.show()
    elif mode == 2:
        import matplotlib.pyplot as plt
        import numpy as np
        # 内层数据
        inner_x = [200, 101, 94, 180]
        inner_labels = ['中', '美', '俄', '德']

        # 外层数据
        outer_x = [120, 80, 26, 75, 26, 68, 89, 91]
        outer_labels = ['纺织品', '稀土', '大豆', '芯片', '天然气', '武器', '电子', '汽车']

        # 饼图颜色映射
        cmap = plt.colormaps["tab20c"]
        #大类颜色,0,4,8
        outer_colors = cmap(np.arange(4)*4)
        #子类颜色,分布在大类区间范围,可以使同类色系一致
        inner_colors = cmap([1, 2, 5,6, 8,9, 10, 11])

        plt.figure(figsize=(10, 10))
        # 绘制内层饼图
        plt.pie(inner_x,
        labels=inner_labels,
        radius=0.5,
        #autopct=lambda pct: ),
        autopct=lambda pct: f"{pct:.1f}%\n({int(pct / 100 * sum(inner_x))})",

        labeldistance=0.25,
        colors=outer_colors,
        wedgeprops=dict(width=0.5, edgecolor='white'))

        # 绘制外层饼图
        plt.pie(outer_x,
        labels=outer_labels,
        radius=1,
        labeldistance=0.75,
        autopct=lambda pct: int(pct / 100 * sum(outer_x)),
        colors=inner_colors,
        wedgeprops=dict(width=0.5, edgecolor='white'))
        #设置绘图风格,支持中文
        set_style_and_chinese(plt)
        plt.title("嵌套饼图(nested pie) - 假设的国际贸易出口", fontsize=16)  # 添加标题
        plt.legend(inner_labels, fontsize=15)
        plt.show()
    else:
        dbg.dbg_info("err",1,"mode not matched!!\n")
    return


#面积图
def draw_area():
    # 创建数据
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # 绘制面积图
    sns.lineplot(x=x, y=y1, label='sin(x)')
    sns.lineplot(x=x, y=y2, label='cos(x)')
    plt.fill_between(x, y1, color='blue', alpha=0.5)
    plt.fill_between(x, y2, color='red', alpha=0.5)

    # 添加标题和标签
    set_style_and_chinese(plt)
    plt.title('面积图(Area Plot)')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()

    # 显示图形
    plt.show()
    return

#桑基图
def draw_sankey():
    mode = 2
    if mode == 1:
        #这种方式的sankey比较丑
        # 创建一个 Sankey 对象
        sankey = Sankey()
        # 添加流
        sankey.add(flows=[0.25, 0.15, 0.60, -0.20, -0.15, -0.10, -0.40, -0.20],
                labels=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
                orientations=[-1, 1, 0, 1, -1, -1, 0, -1])

        # 绘制桑基图
        diagrams = sankey.finish()
        for diagram in diagrams:
            diagram.text.set_fontweight('bold')
        # 显示图形
        set_style_and_chinese(plt)
        plt.title('桑基图(Sankey Diagram)')
        plt.show()
    elif mode == 2:
        # 定义数据
        labels = ["A", "B", "C", "D", "E"]

        # source和target成对应关系,这里的定义,索引为0的流向了索引为1,索引为2的两部分
        source = [0, 0, 1, 2, 3]  # 源节点索引
        target = [1, 2, 3, 3, 4]  # 目标节点索引
        value = [10, 15, 20, 5, 10]  # 流量值

        # 创建桑基图
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color="yellow"
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )])
        set_style_and_chinese(plt)
        # 更新布局
        fig.update_layout(
            title_text="桑基图(Sankey Diagram)",
            font_size=16,
            height=600,
            width=800
        )
        # 显示图形
        fig.show()
    else:
        #do nothing
        print("mode unknown!!")
    return

#地图
def draw_map():
    mode = 1
    if mode == 1:
        # 加载数据
        df = px.data.gapminder().query("country=='China'")
        # 绘制散点地图
        fig = px.scatter_geo(df, locations="iso_alpha", color="lifeExp",
                            hover_name="country", size="gdpPercap",
                            animation_frame="year", projection="natural earth")
        # 添加标题
        set_style_and_chinese(plt)
        fig.update_layout(title="世界地图(World Map)")

        # 显示图形
        fig.show()
    elif mode == 2:
        # 加载世界地图数据
        # 问题：AttributeError: module 'fiona' has no attribute 'path',geopandas==0.13.2,fiona==1.10.0
        # 解决：更新geopandas==0.14.4或固定fiona到版本1.9.6
        # pip show fiona 查看版本号
        # pip install fiona==1.9.6 安装指定版本
        #shapefile_path = './dataset/tiger-data/ne_110m/ne_110m_admin_0_countries.shp'
        #world = gpd.read_file(shapefile_path)

        # 加载世界地图数据
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        # 创建一个示例分类数据集
        data = {
            'iso_a3': ['USA', 'CAN', 'MEX', 'BRA', 'CHN'],  # 国家代码
            'category1': [30, 20, 10, 40, 50],
            'category2': [20, 30, 40, 30, 20],
            'category3': [50, 50, 50, 30, 30]
        }

        # 创建 DataFrame
        data_df = pd.DataFrame(data)

        print(world.columns)

        # 将分类数据与世界地图数据合并
        world = world.merge(data_df, on='iso_a3', how='left')

        # 查看合并后的数据
        print(world.head())

        # 创建地图
        fig, ax = plt.subplots(figsize=(15, 10))

        # 绘制世界地图底图
        world.plot(ax=ax, color='lightblue', edgecolor='black', alpha=0.5)

        # 遍历每个国家,绘制符号饼图
        for idx, row in world.iterrows():
            if pd.notnull(row['category1']):  # 确保数据存在
                # 获取分类数据
                categories = [row['category1'], row['category2'], row['category3']]
                labels = ['Category 1', 'Category 2', 'Category 3']
                colors = ['red', 'green', 'blue']
                
                # 计算饼图的中心位置(国家的几何中心)
                centroid = row['geometry'].centroid
                x, y = centroid.x, centroid.y
                
                # 绘制饼图
                ax.pie(categories, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140,
                    center=(x, y), radius=1, wedgeprops=dict(width=0.3))

        # 设置标题
        ax.set_title('Symbol Pie Chart on World Map', fontsize=16)
        ax.set_axis_off()  # 关闭坐标轴

        # 显示地图
        plt.show()

    elif mode == 3: 
        # 提供的数据
        data = {
            '省/市': ['河南省', '广东省', '山东省', '四川省', '安徽省', '河北省', '贵州省', '湖南省', '广西壮族自治区',
                    '江西省', '湖北省', '江苏省', '陕西省', '山西省', '云南省', '浙江省', '甘肃省', '重庆市', '辽宁省',
                    '内蒙古自治区', '福建省', '黑龙江省', '新疆维吾尔自治区', '吉林省', '宁夏回族自治区', '北京市', '海南省',
                    '天津市', '上海市', '青海省', '西藏自治区'],
            '2017年': [86.3, 75.7, 58.3, 58.3, 49.9, 43.6, 41.2, 41.1, 36.5, 36.5, 36.2, 33.0, 31.9, 31.7, 29.3, 29.1, 28.5,
                    21.1, 20.8, 19.8, 18.8, 18.8, 18.4, 14.3, 6.9, 6.0, 5.7, 5.7, 5.0, 4.6, 2.8]
        }            
        # 数据处理,将省份名称和对应的高考人数组成元组列表 
        province_data = [(province, num) for province, num in zip(data['省/市'], data['2017年'])]
        # 使用 Map 类生成地图
        china_map = (
            Map()
            .add("2017年高考人数(万人)", province_data, "china")
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False, formatter="{c}", position="inside")
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=90, is_piecewise=True),
                title_opts=opts.TitleOpts(title="2017年中国各省高考人数"),
            )
        )
        # 生成本地html文件 
        # 问题！！,依赖外部js文件,网络屏蔽后会导致显示空白
        china_map.render("./dataset/tiger-data/中国高考人数地图.html")

    elif mode == 4:
        # 读取自带世界地图数据集
        #countries = r'./dataset/tiger-data/ne_110m/ne_110m_admin_0_countries.shp'
        #cities = r'./dataset/tiger-data/ne_110m/ne_110m_admin_1_states_provinces.shp'
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        # 人口,大洲,国名,国家缩写,ISO国家代码,gdp,地理位置数据
        # 检查数据集的列名
        print("Columns in the GeoDataFrame:", world.columns)
        # 查看数据
        print(world.head())
        # 问题！！！,geopandas已更新,对应的自带数据集合以及world接口方法存在变化,此处去除南极洲失败
        # 'GeoDataFrame' object has no attribute 'pop_est'
        # 使用 pip install GeoPandas==0.10.2 ,该库固定到0.10.2版本可以支持
        # 去除南极地区
        world = world[(world.pop_est>0) & (world.name!="Antarctica")]
        # 计算人均gpd
        world['gdp_per_cap'] = world.gdp_md_est / world.pop_est
        # 绘图
        world.plot(column='gdp_per_cap')
        #world.plot()
        plt.show()
    else:
        print("unknow mode!!")
    return

#气泡图
def draw_bubble():
    # 示例数据
    countries = ['USA', 'China', 'Japan', 'Germany', 'India']
    gdp = [21.4, 14.3, 5.1, 3.9, 3.2]  # GDP (万亿美元)
    population = [331, 1439, 126, 83, 1380]  # 人口 (百万)
    unemployment_rate = [3.6, 3.9, 2.4, 3.1, 7.6]  # 失业率 (%)

    # 创建气泡图
    plt.figure(figsize=(10, 6))
    plt.scatter(unemployment_rate, gdp, s=[p * 10 for p in population], alpha=0.5, c='blue')

    # 添加标签和标题
    for i, txt in enumerate(countries):
        plt.annotate(txt, (unemployment_rate[i], gdp[i]), fontsize=9)

    set_style_and_chinese(plt)
    plt.xlabel('失业率-Unemployment Rate (%)')
    plt.ylabel('GDP (Trillion USD)')
    plt.title('气泡图(Bubble) - GDP vs Unemployment Rate with Population Size')
    plt.grid(True)
    plt.show()
    return

#韦恩图
def draw_venn():
    #3个以内的集合直接使用venn库,超出三个的venn不支持,
    #接口如此设计是合理的,venn上太多的圈,不方便清晰的展示多个圈之间的关系,
    # 你就想要表示1个圈和其他3个圈的交集就很不好绘制了
    # 定义3个随机集合,定义集合的大小范围
    arry_size = 20
    min_value = 1
    max_value = 100
    set_a = {random.randint(min_value, max_value) 
            for _ in range(arry_size)}
    
    arry_size = 100
    min_value = 50
    max_value = 150
    set_b = {random.randint(min_value, max_value) 
            for _ in range(arry_size)}
    
    arry_size = 80
    min_value = 25
    max_value = 200
    set_c = {random.randint(min_value, max_value) 
            for _ in range(arry_size)}

    # 绘制维恩图, 3个集合就是venn3
    venn3([set_a, set_b, set_c], set_labels=('Set A', 'Set B','Set C'), 
        set_colors=('red', 'blue', 'yellow'), alpha=0.5)

    # 添加标题
    set_style_and_chinese(plt)
    plt.title('韦恩图(Venn Diagram)', fontsize=16)

    # 显示图表
    plt.show()
    return

#多集合图
def draw_upset(): 
    mode = 2
    if mode == 1:      
        # demo 1, 使用generate_counts构造
        example = generate_counts()
        if isinstance(example.index, pd.MultiIndex):
            print("索引是 MultiIndex")
        else:
            print("索引不是 MultiIndex")
        print(example,"\n\n")
        '''
        example数据：
        cat0   cat1   cat2 
        False  False  False      56
                    True      283
            True   False    1279
                    True     5882
        True   False  False      24
                    True       90
            True   False     429
                    True     1957
        Name: value, dtype: int64
        [重要！！！]  用于绘图的分类需要作为索引,且为BOOL型组合
        Level 0 (cat0): [False, True]
        Level 1 (cat1): [False, True]
        Level 2 (cat2): [False, True]
        '''
        # 获取 MultiIndex 的所有级别
        levels = example.index.levels
        # 打印每个级别的所有唯一值
        for i, level in enumerate(levels):
            print(f"Level {i} ({example.index.names[i]}): {list(level)}")
        print("\n\n")
        # 绘制 UpSetPlot
        upset_plot(example)
        plt.title('UpSet Plot of Four Sets')
        plt.show()     
    elif mode == 2:
        from upsetplot import generate_counts, plot
        # demo 2, 自定义构造
        # 生成随机集合,注意这里不能是list,会导致随机出现重复值,导致绘图失败
        set_a = {random.randint(1, 100) for _ in range(random.randint(10, 50))}
        set_b = {random.randint(50, 150) for _ in range(random.randint(10, 60))}
        set_c = {random.randint(90, 200) for _ in range(random.randint(10, 80))}
        set_d = {random.randint(30, 300) for _ in range(random.randint(10, 100))}
        # 打印生成的集合
        print("Set A:", set_a)
        print("Set B:", set_b)
        print("Set C:", set_c)
        print("Set D:", set_d)
        data = {"A":set_a,"B":set_b,"C":set_c,"D":set_d}

        # 转换为upsetplot需要的格式
        # [重要！！！] data的格式,需要是一个字典,
        # 其中键是集合名称,值是集合中包含的元素列表。这些元素必须是 int 或 str 格式,且单个集合中元素不能出现重复
        upset_data = from_contents(data)
        print(upset_data)

        # 验证索引是否为 MultiIndex
        if isinstance(upset_data.index, pd.MultiIndex):
            print("索引是 MultiIndex")
        else:
            print("索引不是 MultiIndex")
        # 绘制 UpSetPlot
        plot(upset_data, facecolor="darkblue")
        #upset_plot(upset_data)
        set_style_and_chinese(plt)
        # 使用 seaborn-darkgrid 样式表
        #print(plt.style.available)
        plt.title('多集合图(UpSet Plot)', fontsize=16)
        plt.show()
    else:
        print("unknow mode!!")
    return


#词云图
def draw_wordcloud():
    # 示例文本数据
    text = """
    人工智能(Artificial Intelligence,简称AI)是计算机科学的重要分支,旨在模拟和扩展人类的智能。
    通过机器学习、深度学习、自然语言处理等技术,AI能够执行复杂任务,如图像识别、语音交互、数据分析和
    决策支持。近年来,随着算法优化和算力提升,AI已广泛应用于医疗、金融、教育、交通等领域,
    显著提高了效率并推动了创新。然而,AI的发展也带来伦理和社会挑战,如隐私保护、就业影响等。
    未来,AI将继续深化与人类社会的融合,在增强人类能力的同时,也需要合理的监管与引导,
    以实现科技与人文的平衡发展
    """
    # 创建词云对象
    # [注意！！！] 此处需要配置指定中文字体路径,否则会导致中文显示乱码
    font_path = "C:\\Windows\\Fonts\\msyh.ttc"  # 微软雅黑字体路径
    wordcloud = WordCloud(
        font_path=font_path,
        width=800,  # 词云图的宽度
        height=400,  # 词云图的高度
        background_color='white',  # 背景颜色
        max_words=100,  # 最大显示的词数
        min_font_size=10,  # 最小字体大小
        max_font_size=100,  # 最大字体大小
        random_state=42  # 随机种子,用于生成可重复的结果
    ).generate(text)

    # 显示词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    set_style_and_chinese(plt)
    plt.title('词云图(Word Cloud)', fontsize=16)
    plt.axis('off')  # 关闭坐标轴
    plt.show()
    return

#维诺图
def draw_voronoi():
    mode = "2D"
    if mode == "2D":
        # 生成随机点
        points = np.random.rand(20, 2)
        # 计算维诺图
        vor = Voronoi(points)
        # 绘制维诺图
        voronoi_plot_2d(vor)
        set_style_and_chinese(plt)
        plt.title('维诺图(Voronoi)', fontsize=16)
        plt.show()
    elif mode == "3D":
        # 生成随机点
        points = np.random.rand(10, 3)  # 生成 10 个随机的 3D 点
        # 计算维诺图
        vor = Voronoi(points)
        # 绘制维诺图
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # 绘制每个维诺单元
        for simplex in vor.ridge_vertices:
            if all(i >= 0 for i in simplex):  # 忽略无限远的边
                poly = [vor.vertices[i] for i in simplex]
                ax.add_collection3d(Poly3DCollection([poly], alpha=0.25))
        # 绘制生成元点
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='red')

        # 设置图形范围
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)

        # 显示图形
        set_style_and_chinese(plt)
        plt.title('维诺图(Voronoi)', fontsize=16)
        plt.show()
    else:
        dbg.dbg_info("err",1,"mode not matched!!\n")
    return

# 金字塔图
def draw_pyramid():
    mode = "population"
    if mode == "population":
        # 示例数据：不同年龄组的男性和女性人口数量
        age_groups = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61+']
        male_population = [100, 150, 200, 250, 300, 350, 400]
        female_population = [120, 160, 210, 260, 310, 360, 410]

        # 将男性人口数量取负值,以便在图中显示在左侧
        male_population = [-x for x in male_population]

        # 创建图形和轴
        fig, ax = plt.subplots()

        # 绘制男性人口
        ax.barh(age_groups, male_population, color='blue', label='Male')
        # 绘制女性人口
        ax.barh(age_groups, female_population, color='pink', label='Female')

        # 添加图例
        ax.legend()

        # 设置标题和标签
        ax.set_xlabel('Population')
        ax.set_ylabel('Age Group')
        # 设置 x 轴的范围
        ax.set_xlim(-450, 450)
        # 显示网格
        ax.grid(True)
        # 显示图形
        set_style_and_chinese(plt)
        plt.title('金字塔图(Pyramid) - Population', fontsize=16)
        plt.show()
    elif mode == "Maslow":  #Maslow's Hierarchy of Needs
        # 马斯洛需求层次理论的五个层次及其描述
        levels = [
            "生理需求(Physiological Needs)",
            "安全需求(Safety Needs)",
            "爱与归属需求(Love and Belongingness Needs)",
            "尊重需求(Esteem Needs)",
            "自我实现需求(Self-Actualization Needs)"
        ]

        # 每个层次的宽度(可以调整以反映不同层次的重要性)
        widths = [8, 6, 4, 2, 1]

        # 创建图形和轴
        fig, ax = plt.subplots()

        # 绘制金字塔
        for i, level in enumerate(levels):
            ax.barh(i, widths[i], color='skyblue', edgecolor='black')

        # 添加层次标签
        for i, level in enumerate(levels):
            ax.text(widths[i]+1, i, level, ha='left', 
            va='center', fontsize=10, color='black')

        # 设置图形范围和标签
        ax.set_xlim(0, max(widths) + 1)
        #ax.set_yticks(range(len(levels)))
        #ax.set_yticklabels(levels)
        ax.set_xlabel('需求层次')
        ax.set_title('马斯洛需求层次理论金字塔图')

        # 隐藏右侧和顶部的边框
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        #设置绘图风格,支持中文
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

        # 显示图形
        plt.show()
    else:
        dbg.dbg_info("err",1,"mode not matched!!\n")
    return

#漏斗图
def draw_funnel():
    import plotly.express as px
    stages = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"]
    df_mtl = pd.DataFrame(dict(number=[39, 27.4, 20.6, 11, 3], stage=stages))
    df_mtl['office'] = 'Montreal'
    df_toronto = pd.DataFrame(dict(number=[52, 36, 18, 14, 5], stage=stages))
    df_toronto['office'] = 'Toronto'
    df = pd.concat([df_mtl, df_toronto], axis=0)
    fig = px.funnel(df, x='number', y='stage', color='office')
    # 添加标题
    fig.update_layout(
        title={
            'text': "漏斗图(Funnel) - 客户转化率",  # 标题文本
            'y': 0.95,  # 标题的 y 位置
            'x': 0.5,  # 标题的 x 位置
            'xanchor': 'center',  # 标题的水平锚点
            'yanchor': 'top'  # 标题的垂直锚点
        }
    )
    fig.show()
    return

#树形图
def draw_tree():
    import networkx as nx
    import matplotlib.pyplot as plt
    # 创建一个有向图
    G = nx.DiGraph()
    # 添加节点和边
    nodes = ["Root", 
             "Child 1", "Child 2", 
             "Grand 1.1", "Grand 1.2",
             "Grand 2.1", "Grand 2.2",
             "Great-Grand 1.1.1","Great-Grand 1.1.2",
             "Great-Grand 2.1.1", "Great-Grand 2.1.2"]
    edges = [("Root", "Child 1"),
            ("Root", "Child 2"),
            ("Child 1", "Grand 1.1"),
            ("Child 1", "Grand 1.2"),
            ("Child 2", "Grand 2.1"),
            ("Child 2", "Grand 2.2"),
            ("Grand 1.1", "Great-Grand 1.1.1"),
            ("Grand 1.1", "Great-Grand 1.1.2"),
            ("Grand 2.1", "Great-Grand 2.1.1"),
            ("Grand 2.1", "Great-Grand 2.1.2")]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # 使用Spring布局来排列节点
    #pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 10))    
    set_style_and_chinese(plt)
    plt.title('树形图(Tree Diagram) - 继承关系', fontsize=16)
    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", 
        font_size=12, arrows=True)
    # 绘制图形
    plt.show()

    return

#矩形树形图
def draw_treemap():
    # 随机10个分类,分类名称,颜色,数值,均随机
    itemNums = 10
    sizes = [random.randint(0, 1000) for i in range(itemNums)]
    labels = ''.join(random.choice(string.ascii_letters) for _ in range(itemNums))  
    colors = [("#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])) for _ in range(itemNums)]
    # 绘制矩形树图
    plt.figure(figsize=(8, 6))
    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.7)
    plt.axis('off')
    set_style_and_chinese(plt)
    plt.title("矩形树图(Tree Map)", fontsize=16)
    plt.show()
    return

#人物关系图
def draw_relationship():
    import utils_random
    roles = ['Alice','Bob', 'Charlie','David','Eve','Fiona','Gary','Tom','Jessy','Lucy']
    relationships = utils_random.rand_relations(roles)

    # 创建有向图
    G = nx.DiGraph()

    # 添加节点和边
    for person, related in relationships.items():
        G.add_node(person)  # 添加节点
        for rel in related:
            G.add_edge(person, rel)  # 添加边
    
    # 使用spring布局
    pos = nx.spring_layout(G)

    # 绘制图形
    plt.figure(figsize=(10,10))
    set_style_and_chinese(plt)
    plt.title('人物关系图(Relationship) - 随机人物关系',fontsize=16)
    node_colors = ['red' if person == 'Alice' else 'skyblue' for person in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_size=8)
   
    plt.show()

    return

#帕累托图
def draw_pareto():
    # 示例数据
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [23, 45, 12, 8, 67]

    # 按值从大到小排序
    sorted_indices = np.argsort(values)[::-1]
    categories = [categories[i] for i in sorted_indices]
    values = [values[i] for i in sorted_indices]

    # 计算累积百分比
    cumulative_percentage = np.cumsum(values) / sum(values) * 100

    # 绘制柱状图
    fig, ax1 = plt.subplots()
    set_style_and_chinese(plt)

    ax1.bar(categories, values, color='skyblue')
    ax1.set_xlabel('Categories')
    ax1.set_ylabel('Frequency', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # 绘制折线图
    ax2 = ax1.twinx()
    ax2.plot(categories, cumulative_percentage, color='tab:red', marker='o', linestyle='--')
    ax2.set_ylabel('Cumulative Percentage', color='tab:red')
    ax2.set_ylim(0, 100)
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # 添加网格线
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # 添加标题
    plt.title('帕累托图(Pareto Chart) - 异常分类频次统计',fontsize=16)

    # 显示图表
    plt.show()


def main():
    #draw_histogram()
    #draw_bar()
    #draw_heatmap()
    #draw_boxplot()
    #draw_kde()
    #draw_violinplot()
    #draw_scatter_matrix()
    #draw_hexbin()
    #draw_pie()
    #draw_multipie()
    #draw_area()
    #draw_sankey()
    #draw_map()
    #draw_bubble()
    #draw_venn()
    #draw_upset()
    #draw_wordcloud()
    #draw_voronoi()
    #draw_pyramid()
    #draw_funnel()
    #draw_tree()
    #draw_treemap()
    #draw_relationship()
    draw_pareto()
    return

if __name__ == '__main__':
    main()







