# -*- coding: utf-8 -*-
# UI界面

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import curves
import dynamic
import graph
import debug as dbg


# 模拟的函数，实际使用时替换为您的工具库函数
def show_static_graph():
    print("展示静态图功能")

def show_dynamic_graph():
    print("展示动态图功能")

def show_function_graph():
    print("展示函数图功能")

def show_function_graph1():
    print("展示函数图功能1111")


class DemoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("数据分析及绘图工具库演示")
        self.root.geometry("800x600")
        
        # 设置ttkbootstrap主题
        self.style = tb.Style(theme="minty")
        
        # 创建主框架
        self.main_frame = tb.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题
        self.title_label = tb.Label(
            self.main_frame, 
            text="数据分析及绘图工具库演示", 
            font=('Helvetica', 18, 'bold'),
            bootstyle=PRIMARY
        )
        self.title_label.pack(pady=(0, 20))
        
        # 创建Notebook用于分类展示
        self.notebook = tb.Notebook(self.main_frame, bootstyle=PRIMARY)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = tb.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bootstyle=(PRIMARY, INVERSE)
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

        # 静态图标签页
        self.static_frame = tb.Frame(self.notebook)
        self.notebook.add(self.static_frame, text="静态图模块")
        self.create_static_tab()
        
        # 动态图标签页
        self.dynamic_frame = tb.Frame(self.notebook)
        self.notebook.add(self.dynamic_frame, text="动态图模块")
        self.create_dynamic_tab()
        
        # 函数图标签页
        self.function_frame = tb.Frame(self.notebook)
        self.notebook.add(self.function_frame, text="函数图模块")
        self.create_function_tab()
        
    def auto_create_demo_buttons(self,root, functions_info, colNums=4,tabname=""):
        """
        自动创建演示按钮
        :param root: 父容器(窗口或Frame)
        :param functions_info: 包含函数信息的列表，每个元素是(name, func)元组
        """
        row = 0
        col = 0
        for i, (name, func) in enumerate(functions_info):
            print(i,"--", name,func)
            btn = tb.Button(
                root,
                text=f"{name}",
                #[注意！！！]此处这样写会有一个bug导致所有的按钮都是最后一个函数，lambda函数在循环中的变量作用域和闭包延迟绑定导致的
                #command=lambda：self.run_demo(f"{tabname}: {name}", func),
                #有以下几个概念需要注意：
                #0. Lambda表达式， 语法： lambda param : expression ， 可以有无限个param，但只能有一个expression
                #1. 闭包（Closure）能够访问其他函数作用域中变量的函数，即使那个外部函数已经执行完毕，闭包有两部分组成：一个内部函数，一个外部的变量环境
                #2. 闭包延迟绑定（Late Binding）闭包中的变量不是在定义时查找值，而是在调用时才查找值
                #解决闭包延迟绑定的问题，有以下方法：
                #1. 使用默认参数立即绑定
                #2. 使用functools.partial,显式立即求值
                #3. 工厂函数
                command=lambda f=func,tname=f"{tabname}: {name}" : self.run_demo(tname, f),
                width=15,
                bootstyle=SUCCESS
            )
            if (i) % colNums == 0 and i != 0:
                row = row+1
                col = 0
            btn.grid(row=row, column=col, padx=10, pady=10)
            col = col+1
        return

    def create_static_tab(self):
        """创建静态图模块的界面"""
        #功能函数
        static_functions_list = [
            ("直方图", graph.draw_histogram),
            ("柱状图", graph.draw_bar),
            ("箱线图", graph.draw_boxplot),
            ("概率密度图", graph.draw_kde),
            ("小提琴图", graph.draw_violinplot),
            ("散点图", graph.draw_scatter_matrix),
            ("六边形箱图", graph.draw_hexbin),
            ("饼图", graph.draw_pie),
            ("热力图", graph.draw_heatmap),
            ("面积图", graph.draw_area),
            ("桑基图", graph.draw_sankey),
            ("地图", graph.draw_map),
            ("气泡图", graph.draw_bubble),
            ("韦恩图", graph.draw_venn),
            ("集合图", graph.draw_venn),
            ("词云图", graph.draw_wordcloud),
            ("维诺图", graph.draw_voronoi),
            ("金字塔图", graph.draw_pyramid),
            ("漏斗图", graph.draw_funnel),
            ("树图", graph.draw_tree),
            ("矩形树图", graph.draw_treemap),
            ("人物关系图", graph.draw_relationship)
            ]
        # 说明标签
        desc_label = tb.Label(
            self.static_frame,
            text="静态图模块提供各种静态数据可视化功能",
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        desc_label.pack(pady=(10, 20))

        # 功能按钮框架
        btn_frame = tb.Frame(self.static_frame)
        btn_frame.pack(pady=10)

        # 遍历功能接口创建按钮
        self.auto_create_demo_buttons(btn_frame,static_functions_list,4,"静态图")
        return
    
    def create_dynamic_tab(self):
        """创建动态图模块的界面"""
        #功能函数
        dynamic_functions_list = [
            ("动态折线", dynamic.draw_dynamic_linechart),
            ("动态排名", dynamic.draw_dynamic_rankbar),
            ]
        # 说明标签
        desc_label = tb.Label(
            self.dynamic_frame,
            text="动态图模块提供交互式和动画可视化功能",
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        desc_label.pack(pady=(10, 20))

        # 功能按钮框架
        btn_frame = tb.Frame(self.dynamic_frame)
        btn_frame.pack(pady=10)

        # 遍历功能接口创建按钮
        self.auto_create_demo_buttons(btn_frame,dynamic_functions_list,4,"动态图")
        return

        
    
    def create_function_tab(self):
        """创建函数图模块的界面"""
        #功能函数
        curves_functions_list = [
            ("正弦函数", curves.draw_curve),
            ("螺旋线", curves.draw_curve),
            ]
        # 说明标签
        desc_label = tb.Label(
            self.function_frame,
            text="函数图模块提供数学函数可视化功能",
            font=('Helvetica', 12),
            bootstyle=INFO
        )
        desc_label.pack(pady=(10, 20))
        
        # 功能按钮框架
        btn_frame = tb.Frame(self.function_frame)
        btn_frame.pack(pady=10)
        
        # 遍历功能接口创建按钮
        self.auto_create_demo_buttons(btn_frame,curves_functions_list,4,"函数图")
        return


    
    def run_demo(self, demo_name, demo_func):
        """运行演示函数"""
        self.status_var.set(f"正在运行: {demo_name}...")
        self.root.update()
        
        try:
            demo_func()
            self.status_var.set(f"完成: {demo_name}")
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")

if __name__ == "__main__":
    root = tb.Window()
    app = DemoUI(root)
    root.mainloop()




'''
def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("Tkinter")

    # 创建按钮
    button = tk.Button(root, text="y=sin(x)", command=lambda: curves.draw_curve("sin"))
    button.pack(pady=10)

    button = tk.Button(root, text="helix", command=lambda: curves.draw_curve("helix"))
    button.pack(pady=10)

    # 创建标签用于显示结果
    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack(pady=20)

    # 运行主循环
    root.mainloop()


    root = ttk.Window()
    style = ttk.Style()
    theme_names = style.theme_names()#以列表的形式返回多个主题名
    theme_selection = ttk.Frame(root, padding=(10, 10, 10, 0))
    theme_selection.pack(fill=X, expand=YES)
    lbl = ttk.Label(theme_selection, text="选择主题:")
    theme_cbo = ttk.Combobox(
            master=theme_selection,
            text=style.theme.name,
            values=theme_names,
    )
    theme_cbo.pack(padx=10, side=RIGHT)
    theme_cbo.current(theme_names.index(style.theme.name))
    lbl.pack(side=RIGHT)
    def change_theme(event):
        theme_cbo_value = theme_cbo.get()
        style.theme_use(theme_cbo_value)
        theme_selected.configure(text=theme_cbo_value)
        theme_cbo.selection_clear()
    theme_cbo.bind('<<ComboboxSelected>>', change_theme)
    theme_selected = ttk.Label(
            master=theme_selection,
            text="litera",
            font="-size 24 -weight bold"
    )
    theme_selected.pack(side=LEFT)
    root.mainloop()



    return

if __name__ == '__main__':
    main()

'''



