

import gradio as gr

def greet(name, is_morning, temperature):
    salutation = "Good morning" if is_morning else "Good evening"
    greeting = f"{salutation} {name}. It is {temperature} degrees today"
    celsius = (temperature - 32) * 5 / 9
    return greeting, round(celsius, 2)

# 创建一个Gradio界面的实例。fn参数指定了要运行的函数，inputs参数指定了输入组件的类型和顺序，outputs参数指定了输出组件的类型和顺序。在这里，输入组件依次是文本输入、复选框和滑块，输出组件依次是文本输出和数字输出。
demo = gr.Interface(
    fn=greet,
    # 输入部分为Text组件，checkbox组件、滑块。
    inputs=["text", "checkbox", gr.Slider(0, 100)],
    outputs=["text", "number"],
)
demo.launch()











