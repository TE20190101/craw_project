# encoding:utf-8
# FileName: craw_university_info
# Author:   xiaoyi | 小一
# wechat:   zhiqiuxiaoyi
# 公众号：   小一的学习笔记
# email:    zhiqiuxiaoyi@qq.com
# Date:     2021/5/20 19:25
# Description:爬取全国高校数据：https://gkcx.eol.cn/school/search?
import json
import random
import time

import pandas as pd
import numpy as np
import warnings

import requests

from craw_tools.get_ua import get_ua

warnings.filterwarnings('ignore')

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
# pd.set_option('display.max_rows', None)


def get_size(page=1):
    """
    获取数据总条数
    @param page:
    @return:
    """
    url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page={0}&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&top_school_id=[2941]&type=&uri=apidata/api/gk/school/lists'\
        .format(page)
    res = requests.post(url, headers={'User-Agent': get_ua()})
    data = json.loads(res.text)

    size = 0
    if data["message"] == '成功':
        size = data["data"]["numFound"]

    return size


def get_university_info(size, page_size=20):
    page_cnt = int(size/page_size) if size%page_size==0 else int(size/page_size)+1
    print('一共{0}页数据，即将开始爬取...'.format(page_cnt))

    df_result = pd.DataFrame()
    for index in range(1, page_cnt+1):
        print('正在爬取第 {0}/{1} 页数据'.format(index, page_cnt))
        url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_doublehigh=&is_dual_class=&keyword=&nature=&page={0}&province_id=&ranktype=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&top_school_id=[2941]&type=&uri=apidata/api/gk/school/lists' \
            .format(index)
        res = requests.post(url, headers={'User-Agent': get_ua()})
        data = json.loads(res.text)

        if data["message"] == '成功':
            df_data = pd.DataFrame(data["data"]["item"])
            df_result = df_result.append(df_data)
            time.sleep(random.randint(3, 5))

    return df_result


if __name__ == '__main__':
    size = get_size()

    df_result = get_university_info(size)
    df_result.to_csv('高校数据.csv', encoding='gbk', index=False)
