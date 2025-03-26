import sys
import os

# 打印调用信息
# msgType: info,err,cri
# frameNo：栈帧层数，0表示当前函数，1表示上一层函数，以此类推
# detailStr: 用户自定义详细信息
def dbg_info(msgType,frameNo,detailStr):
    frame = sys._getframe(frameNo)
    # 获取文件名
    file_name = frame.f_code.co_filename
    # 获取函数名
    func_name = frame.f_code.co_name
    # 获取行号
    line_number = frame.f_lineno

    if msgType == 'cri':
        print(f"[CRIT][{file_name}][{func_name}][{line_number}],[{detailStr}]")
    elif msgType == 'err':
        print(f"[ERR][{file_name}][{func_name}][{line_number}],[{detailStr}]")
    else:
        print(f"[INFO][{file_name}][{func_name}][{line_number}],[{detailStr}]")
    return










