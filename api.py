#!/usr/bin/python
# -*- coding: UTF-8 -*-


# https://blog.csdn.net/qq_41564422/article/details/104236425


# 导入(HTTP)网络请求包
import requests
# 导入睡眠时间包
import time
# 导入(自定义)文件包
import file
# 导入读取指定的行包
import linecache
# 导入处理json包
import json


# 爬虫潮汐数据
def analytical_tide(_year, _month, _day):
    year = '%d' % (_year)

    # 设置headers参数
    headers = {
        'Cookie': 'ASP.NET_SessionId=xd4ffcc3ufci5kxpvysykhrh; Hm_lvt_b5310477f7d575e5540bcb3e5a0f5bc5=1637741370; Hm_lvt_6afd6ce62b5ce405eb9d8fe97b6afd89=1637741371; Hm_lvt_85dddb683a771a87a935fba121c03b0f=1637742004; Hm_lpvt_85dddb683a771a87a935fba121c03b0f=1637864488; tideUser=ID=B569248056F115CB31EBA961A533B6442413724BBD2133F2&ExpiresTime=637735764963432890&LoginName=A7871310C862FE1A&LoginTime=AEC6C21A0CEA93871D3B1AFD288F98F3DE9F6C941BD0A765; Hm_lpvt_b5310477f7d575e5540bcb3e5a0f5bc5=1637864493; Hm_lpvt_6afd6ce62b5ce405eb9d8fe97b6afd89=1637864493',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X -1_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Origin': 'http://global-tide.nmdis.org.cn',
        'Referer': 'http://global-tide.nmdis.org.cn/Site/Site.html',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }
    # 爬取前五页的评论
    # month = ('%d' % (_month + 1)) if (_month + 1 >= 10) else ("0" + '%d' % (_month + 1))

    day = ('%d' % (_day)) if (_day >= 10) else ("0" + '%d' % (_day))

    # 第一次lasthotcommentid为空
    lasthotcommentid = ''
    params = {
        'ApiRequest': '{"Server":"User","Command":"GetData","Data":{"code":"T174","date":"' + year + '-' + _month + '-' + day + '"}}',
    }
    # 请求与网站的连接
    res = requests.get('http://global-tide.nmdis.org.cn/Api/Service.ashx', headers=headers, params=params)
    # 解析JSON
    data = res.json()
    # print(data)

    str = json.dumps(data)
    dataD = json.loads(str)
    # print(dataD)

    if 'Data' in dataD.keys():
        sub_data = dataD['Data']['SubData']

        j_sub_data=json.dumps(sub_data)
        # print(type(j_sub_data))
        # print("截取后(字符串)数据= "+j_sub_data)

        return j_sub_data
    else:
        print("没有 Data")
        return '{"Day": ' + day +'}'



"""
采集潮汐(含日出日落)数据。【运行此文件前，先运行 analytical.py，并正确生成日出日落数据】

:param year: 请求的年份。
:param _month: 请求开始的月份。
:param month_: 请求结束的月份。

:returns: 没有返回值，生成的结果路径为data文件夹下。
:raises keyError: raises an exception


https://blog.csdn.net/qdPython/article/details/105600553
"""
def tide_data(year, _month, month_):
    path_list = file.Test2(file.PATH)
    for i, month in enumerate(path_list):
        if ((_month - 1) > i or i > (month_ - 1)):
            print("(不)符合月份=" + str(i+1) +"【" + str(_month) + "~" + str(month_) + "】")
            continue
        else:
            print("符合月份=" + str(i+1) +"【" + str(_month) + "~" + str(month_) + "】")

        print("排序后序号:%s => 文件名:%s => 路径:%s" % (i + 1, month, (file.PATH + month)))
        file_path = file.PATH + month
        num_lines = sum(1 for line in open(file_path))
        # print(num_lines)
        for j in range(num_lines):
            day = j + 1
            sunrise_sunset = linecache.getline(file_path, day).strip()
            # print("月份= " + month + "；日=" + ('%d' % (day)) + "；内容=" + sunrise_sunset)
            sub_data = analytical_tide(year, month, day)
            # print("潮汐数据= " + sub_data)

            sub_data_list = list(sub_data)
            sub_data_list.insert(1, sunrise_sunset)
            if (j != 0):
                sub_data_list.insert(0, ',')
            line_data = ''.join(sub_data_list)
            print("【潮汐数据】= " + line_data)
            file.replace_line(file_path, j, line_data)
            time.sleep(0.8) # 防止爬取太快被封

        file.addition_line_(file_path, '{"errorCode": 0,"errorMsg": "","data": {"month": '+ str(i+1) +',"list": [')
        file.addition_line(file_path, "]}}")
        time.sleep(3) # 防止爬取太快被封



print("潮汐数据(开始)===================================================================================================")
tide_data(2021, 11, 12)
print("潮汐数据(结束)===================================================================================================")







