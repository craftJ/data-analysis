# -*- coding: utf-8 -*-
# UI界面

import tkinter as tk
import curves

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
    return

if __name__ == '__main__':
    main()





