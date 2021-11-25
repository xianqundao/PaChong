#!/usr/bin/python
# -*- coding: UTF-8 -*-


# 导入网络请求包
import urllib.request
# 导入网络请求错误码包
import urllib.error
# 导入SSL认证包
import ssl
# 导入解析HTML包
from bs4 import BeautifulSoup
# 导入睡眠时间包
import time
# 导入处理文件包
import os
# 导入(自定义)文件包
import file


"""
采集日出日落数据。

:param _year: 请求的年份。

:returns: 没有返回值，生成的结果路径为data文件夹下。
:raises keyError: raises an exception


https://blog.csdn.net/qdPython/article/details/105600553
"""
def analytical_data(_year):
    ssl._create_default_https_context = ssl._create_unverified_context  # SSL验证
    year = '%d' %_year
    for i in range(12):
        month = ('%d' % (i + 1)) if (i + 1 >= 10) else ("0" + '%d' % (i + 1))
        url = "https://richurimo.bmcx.com/jianghongzhen__time__" + year + "_" + month + "__richurimo/"

        # path = os.path.expanduser(r"~/Desktop/" + year + month + ".txt")
        # path = os.path.expanduser(os.path.split(os.path.realpath(__file__))[0] +"/data/" + month)
        # print("文件路径= ", file.PATH + month)
        path = os.path.expanduser(file.PATH + month)
        isExist = file.is_file_exist(path)

        try:
            response = urllib.request.urlopen(url)
            # print('请求成功：'+response.read().decode('utf-8'))

            html_doc = response.read().decode('utf-8')
            # 创建一个BeautifulSoup解析对象
            soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")

            # 获取目标表格
            table = soup.find_all(name="table", attrs={"width": "100%"
                , "border": "0"
                , "cellpadding": "8"
                , "cellspacing": "1"})
            # print(table)

            trList = table[0].find_all(name='tr')
            for i, tr in enumerate(trList):

                if (i != 0):
                    # text = tr.get_text()
                    # print("需要这个= ", text)
                    tdList = tr.find_all(name='td')
                    date = tdList[0].get_text()
                    sunrise = tdList[1].get_text()
                    sunset = tdList[3].get_text()
                    json = '"date":"' + date + '","sunrise":"' + sunrise + '","sunset":"' + sunset + '",'

                    if (isExist):# 判断文件是否存在
                        if (i == 1):
                            file.write_file(path, json, True)
                        else:
                            file.write_file(path, "\n" + json, False)

                    # read_file(path)
                    else:
                        file.create_file(path)
                        file.write_file(path, json, False)
                        # read_file(path)

                    # print("日期= ", date)
                    # print("日出= ", sunrise)
                    # print("日落= ", sunset)
                    # print("结果= {" + json + "}")
            print("完成[" + year + month + "]日出日落数据" + ("(追加)" if isExist else "(新建)"))

        except urllib.error.HTTPError as e:
            print('响应码: ' + e.code + '\n')
            print('响应: ' + e.reason + '\n')
            print('响应头: ' + e.headers + '\n')
            print("出错[" + year + month + "]日出日落数据")

        # time.sleep(3) # 防止爬取太快被封



analytical_data(2021)
