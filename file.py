#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
# 导入排序包
import numpy as np


# https://juejin.cn/post/6844903827259260942
# https://www.brbtyt.com/key/python%E8%AF%BB%E5%8F%96%E6%96%87%E4%BB%B6%E7%9A%84%E8%B7%AF%E5%BE%84.html

# path_list = os.getcwd()  # 返回当前进程的工作目录
# path = os.path.expanduser(r"~/Desktop/" + year + month + ".txt")
PATH = os.path.split(os.path.realpath(__file__))[0] + "/data/"


# 读文件
def read_file(path):
    f = open(path, 'rb')
    str = f.readlines()
    print(str)
    f.close()


# 读文件(按行)
def read_lines(file_path):
    count = 0
    thefile = open(file_path)
    while True:
        buffer = thefile.read(1024 * 8192)
        if not buffer:
            break
        count += buffer.count('\n')
    thefile.close()


# 写文件
def write_file(path, line, is_truncate):
    # if (os.path.getsize(path) > 0):  # 判断是否为空文件
    with open(path, encoding="utf-8", mode="a") as file:
        if (is_truncate):
            file.seek(0)
            file.truncate() #清空文件
            print("清空文件")
        file.write(line)


# 最前新增新行
def addition_line_(path, _content):
    with open(path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(_content + '\n' + content)

        #     {"errorCode": 0,"errorMsg": "","data": {"month": 11,"list": [
        #         ]}}

        #     {
        #     "errorCode": 0,
        #     "errorMsg": "",
        #     "data": {
        #         "month": 11,
        #         "list": [

        #         ]
        #     }
        # }

# 最后追加新行
def addition_line(path, content):
    with open(path, mode="a") as f:
        f.write(content)
        f.close()


# 根据行号修改文件中指定的行
def replace_line(file_path, line_num, Contents):  # file_path:文件名；line_num：行号；Contents：修改后的内容
    with open(file_path, "r") as f:
        res = f.readlines()  # res 为列表
    # res[line_num - 1] = (Contents + "\n")  # 删除行，因为索引是从 0 开始的，所以需要  -1
    res[line_num] = (Contents + "\n")
    with open(file_path, "w") as f:
        f.write("".join(res))  # 将 res 转换为 字符串重写写入到文本
    return


# 创建文件
def create_file(path):
    # if (is_file_exist(path)):
    open(path, 'w').close()


# 判断文件是否存在
def is_file_exist(path):
    isExist = os.path.exists(path)
    # if isExist:  # 判断是否存在
    #     print("文件存在", path)
    # else:
    #     print("文件(不)存在", path)
    return isExist


# 遍历文件
def Test2(rootDir):

    sort_list = []
    path_list = sorted(os.listdir(rootDir))  # 文件名按字母排序
    # img_nums = len(path_list)
    # for i in range(img_nums):
    #     sort_name = rootDir + path_list[i]
    #     sort_list.append(sort_name) #文件名按数字排序 #https://blog.csdn.net/qq_36481821/article/details/83214167
        # print("文件名= ", sort_name)
    # path_list = os.listdir(rootDir)

    return path_list