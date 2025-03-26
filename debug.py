import sys
import os

def dbg_caller():
    # 获取调用者的帧信息
    frame = sys._getframe(1)  # 1 表示调用栈的上一层
    caller_line_number = frame.f_lineno
    caller_function_name = frame.f_code.co_name
    print(f"func:{caller_function_name}, line:{caller_line_number}")
    return




