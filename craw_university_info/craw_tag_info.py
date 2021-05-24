# encoding:utf-8
# FileName: craw_metro_info_of_sz
# Author:   xiaoyi | 小一
# wechat:   zhiqiuxiaoyi
# 公众号：   小一的学习笔记
# email:    zhiqiuxiaoyi@qq.com
# Date:     2021/4/12 10:46
# Description: 通过名称爬取地点的详细信息，例如：所属区域、经纬度等
import json

import pandas as pd
import warnings
import requests


from craw_tools.get_ua import get_ua
from craw_tools.map import bd09_to_gcj02

warnings.filterwarnings('ignore')

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
# pd.set_option('display.max_rows', None)


def get_data(url):
    """
    获取每一个站点的详细数据
    @param url:
    @return:
    """
    res = requests.get(url, headers={'User-Agent': get_ua()})
    data = json.loads(res.text)
    if len(data["results"]) > 0:
        df_data = pd.DataFrame(data["results"])
        df_data['lat'] = df_data['location'].apply(lambda x: x['lat'])
        df_data['lng'] = df_data['location'].apply(lambda x: x['lng'])
        df_data.drop('location', axis=1, inplace=True)
        # 返回数据
        bd_lng = df_data.loc[0, "lng"]
        bd_lat = df_data.loc[0, "lat"]

        return bd_lng, bd_lat


if __name__ == '__main__':
    filepath = '全国高校数据.csv'
    df_data = pd.read_csv(filepath, encoding='gbk')
    for row_index, data_row in df_data.iterrows():
        region = data_row['province_name']+data_row['city_name']
        query = data_row['name']
        print(query)
        url = 'http://api.map.baidu.com/place/v2/search?query={0}&tag={1}&region={2}&output=json&ak={3}'.format(
            query, "高等院校", region,  ''
        )

        try:
            # 通过百度api获取经度、纬度信息
            bd_lng, bd_lat = get_data(url)
            df_data.loc[df_data['name']==query, 'bd经度'] = bd_lng
            df_data.loc[df_data['name']==query, 'bd纬度'] = bd_lat

            # 通过经纬度转换获取GPS经度、纬度信息
            gps_lng, gps_lat = bd09_to_gcj02(bd_lng, bd_lat)
            df_data.loc[df_data['name']==query, 'gps经度'] = gps_lng
            df_data.loc[df_data['name']==query, 'gps纬度'] = gps_lat
            # excel 三维地图中GPS经纬度需要修正
            df_data.loc[df_data['name']==query, 'gps修正后经度'] = gps_lng+0.00506219000000385
            df_data.loc[df_data['name']==query, 'gps修正后纬度'] = gps_lat-0.00273865999999856
        except:
            print("{0} 爬取失败，请注意！".format(query))
            print(url)

    df_data.to_csv('全国高校数据（带经纬度）.csv', index=False, encoding='gbk')