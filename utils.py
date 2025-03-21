import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from pandas import Series,DataFrame
import inspect
import sys
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm
import os

rawdata_path = "./dataset"

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
    #viridis:从深蓝到黄绿色的渐变。
    #plasma:从深红到黄色的渐变。
    #inferno:从黑色到红色的渐变。
    #magma:从黑色到橙色的渐变。
    #cividis:从深蓝到黄色的渐变。
    #coolwarm:从蓝色到红色的渐变，中间为白色。
    #RdBu:从红色到蓝色的渐变。
    #Blues:从浅蓝到深蓝的渐变。
    #Reds:从浅红到深红的渐变
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

#小提琴图
def draw_violinplot():
    #原始数据读取
    data_path = rawdata_path
    file_name = r"tiger-data/online-shopping.xlsx"
    file_path = os.path.join(data_path, file_name)
    data_read = pd.read_excel(file_path)
    #设置绘图风格,支持中文
    plt.style.use('ggplot')
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
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
                split = True, # 将小提琴图从中间割裂开，形成不同的密度曲线；
                palette = 'RdBu' # 指定不同性别对应的颜色（因为hue参数为设置为性别变量）
                )
    # 添加图形标题
    plt.title('每月消费情况')
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
        df = pd.read_csv("./dataset/seaborn-data/penguins.csv")
        df = df.iloc[:,0:4]
        print(df)

    if 1:
        # 使用 seaborn 绘制散点矩阵图,对角线显示核密度估计
        #kind:用于控制非对角线上的图的类型，可选"scatter"与"reg",对应散点，拟合回归线
        #diag_kind:控制对角线上的图的类型，可选"hist"与"kde"，对应直方图，概率密度估计
        '''
        sns.pairplot(df, diag_kind='kde',kind='reg')
        sns.pairplot(df, diag_kind='kde',kind='scatter')
        sns.pairplot(df, diag_kind='hist',kind='reg')
        '''
        sns.pairplot(df, diag_kind='hist',kind='scatter',hue="species")
        show(plt)
    else:
        # 使用 pandas 绘制散点矩阵图作为比较，
        # 跟想象的不一样，不同的库绘制出来的视觉效果还是比较大的，
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
    show(plt)
    return

#饼图
def draw_pie():
    #mode == 1: 简单饼图
    #mode == 2：嵌套饼图（使用bar，极坐标系方式绘制叠加）
    #mode == 3：嵌套饼图（使用pie绘制叠加）
    mode = 3
    if mode == 1:
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        recipe = ["375 g flour",
                "75 g sugar",
                "250 g butter",
                "300 g berries"]
        data = [float(x.split()[0]) for x in recipe]
        ingredients = [x.split()[-1] for x in recipe]
        def func(pct, allvals):
            absolute = int(np.round(pct/100.*np.sum(allvals)))
            return f"{pct:.1f}%\n({absolute:d} g)"
        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                        textprops=dict(color="w"))
        ax.legend(wedges, ingredients,
                title="Ingredients",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.setp(autotexts, size=8, weight="bold")
        
        ax.set_title("Matplotlib bakery: A pie")

        plt.show()
    elif mode == 2:
        #嵌套饼图采用polar极坐标系
        fig, ax = plt.subplots(subplot_kw=dict(projection="polar"))
        size = 0.3
        vals = np.array([[60., 32.,10.], [37., 40.,33.], [29., 10.,54.]])
        print(vals,"\n")    
        # 数值归一化为弧度
        valsnorm = vals/np.sum(vals)*2*np.pi
        print(valsnorm,"\n")
        # Obtain the ordinates of the bar edges
        # 在极坐标系下，条形图的“ordinates”（纵坐标）实际上是指条形的半径边界值。
        # 注意！！这里使用flatten转换后再cumsum不断累加，达到了不同分类占用弧度的不断累加，方便得到每个大类的开始弧度位置
        valsleft = np.cumsum(np.append(0, valsnorm.flatten()[:-1])).reshape(vals.shape)
        print(valsleft,"\n")

        #饼图颜色映射
        cmap = plt.colormaps["tab20c"]
        #大类颜色，0,4,8
        outer_colors = cmap(np.arange(3)*4)
        #子类颜色，分布在大类区间范围，可以使同类色系一致
        inner_colors = cmap([1, 2, 3, 5, 6, 7, 9, 10,11])
        
        #极坐标/直角坐标系情况下，参数含义分别如下:
        #x:条形图的起始角度（以弧度为单位）  / X轴起始位置
        #width:条形图的宽度（以弧度为单位） / 条形图宽度
        #bottom:条形图的起始半径。         / 条形图底部位置
        #height:条形图的高度（即半径的增量）/ 条形图高度
        #color:条形图的填充颜色 / 同
        #edgecolor:条形图边框的颜色 /同
        #linewidth:条形图边框的宽度/ 同
        #align:条形图的对齐方式。/同
        # 取valsleft第一列，绘制最外圈的大分类，宽度为valsnorm中每行相加，实际就是子类的弧度相加
        ax.bar(x=valsleft[:, 0],
            width=valsnorm.sum(axis=1), bottom=1-size, height=size,
            color=outer_colors, edgecolor='w', linewidth=1, align="edge")

        # 取valsleft所有元素，按照行优先二维转一维，绘制所有子类占比，宽度为子类各自的归一化弧度
        ax.bar(x=valsleft.flatten(),
            width=valsnorm.flatten(), bottom=1-2*size, height=size,
            color=inner_colors, edgecolor='w', linewidth=1, align="edge")

        ax.set(title="nested pie chart")

        #关闭当前坐标轴（axes）的所有轴线（包括刻度、标签和边框）
        ax.set_axis_off()
        plt.show()
    elif mode == 3:
        # 内层数据
        inner_x = [200, 101, 94, 180]
        inner_labels = ['中', '美', '俄', '德']

        # 外层数据
        outer_x = [120, 80, 26, 75, 26, 68, 89, 91]
        outer_labels = ['纺织品', '稀土', '大豆', '芯片', '天然气', '武器', '电子', '汽车']

        plt.figure(figsize=(10, 10))
        #设置绘图风格,支持中文
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        # 绘制内层饼图
        plt.pie(inner_x,
        labels=inner_labels,
        radius=0.5,
        autopct=lambda pct: int(pct / 100 * sum(inner_x)),
        labeldistance=0.25,
        colors=['#d0fefe', '#cb416b', '#0cff0c', 'grey'],
        wedgeprops=dict(width=0.5, edgecolor='white'))

        # 绘制外层饼图
        plt.pie(outer_x,
        labels=outer_labels,
        radius=1,
        labeldistance=0.75,
        autopct=lambda pct: int(pct / 100 * sum(outer_x)),
        colors=['#95d0fc', '#a2cffe', '#ff796c', '#ff028d',
        '#c7fdb5', '#aaff32', '#b9a281', '#d8dcd6'],
        wedgeprops=dict(width=0.5, edgecolor='white'))
        plt.legend(inner_labels, fontsize=15)
        plt.show()
    return

def main():
    #draw_curve("helix")
    #draw_histogram()
    #draw_hist()
    #draw_bar()
    #draw_heatmap()
    #draw_boxplot()
    #draw_kde()
    #draw_violinplot()
    #draw_scatter_matrix()
    #draw_hexbin()
    draw_pie()
    return

if __name__ == '__main__':
    main()







