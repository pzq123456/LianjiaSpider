import hashlib
import random
import sqlite3
import time
import requests
import os
import json
import pandas as pd

PATH = os.path.dirname(os.path.abspath(__file__))
PATH1 = os.path.join(PATH, 'data', 'district_bounds.csv')

SAVE_PATH = os.path.join(PATH, 'result', 'test.txt')


def ua():
    """随机获取一个浏览器用户信息"""

    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
    ]

    agent = random.choice(user_agents)

    return {
        'User-Agent': agent
    }

class Agnet():
    def __init__(self) -> None:
        self.url = 'https://ajax.lianjia.com/map/search/ershoufang/?callback=jQuery1111012389114747347363_1534230881479' \
            '&city_id=%s' \
            '&group_type=%s' \
            '&max_lat=%s' \
            '&min_lat=%s' \
            '&max_lng=%s' \
            '&min_lng=%s' \
            '&filters=%s' \
            '&request_ts=%d' \
            '&source=ljpc' \
            '&authorization=%s' \
            '&_=%d'
        self.cookies = {
                'lianjia_uuid': '9bdccc1a-7584-4639-ba95-b42cf21bbbc7',
                'jzqa': '1.3180246719396510700.1534145942.1534145942.1534145942.1',
                'jzqckmp': '1',
                'ga': 'GA1.2.964691746.1534145946',
                'gid': 'GA1.2.826685830.1534145946',
                'UM_distinctid': '165327625186a-029cf60b1994ee-3461790f-fa000-165327625199d3',
                'select_city': '310000',
                'lianjia_ssid': '34fc4efa-7fcc-4f3f-82ae-010401f27aa8',
                '_smt_uid': '5b72c5f7.5815bcdf',
                'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1537530243',
                'select_city': '110000',
                '_jzqc': '1',
                '_gid': 'GA1.2.178601063.1541866763',
                '_jzqb': '1.2.10.1541866760.1'}
        self.headers = {
            'Host': 'ajax.lianjia.com',
            'Referer': 'https://sh.lianjia.com/ditu/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        self.agent = ua()
        
    def GetMD5(self, string_):
        m = hashlib.md5()
        m.update(string_.encode('utf-8'))
        return m.hexdigest()

    def GetAuthorization(self, dict_) -> str:
        datastr = "vfkpbin1ix2rb88gfjebs0f60cbvhedlcity_id={city_id}group_type={group_type}max_lat={max_lat}" \
                  "max_lng={max_lng}min_lat={min_lat}min_lng={min_lng}request_ts={request_ts}".format(
            city_id=dict_["city_id"],
            group_type=dict_["group_type"],
            max_lat=dict_["max_lat"],
            max_lng=dict_["max_lng"],
            min_lat=dict_["min_lat"],
            min_lng=dict_["min_lng"],
            request_ts=dict_["request_ts"])
        authorization = self.GetMD5(datastr)
        return authorization

# def HoleCityDown(city):  # 爬取小区套数平均价格
#     with sqlite3.connect('district.db') as conn:
#         c = conn.cursor()
#         c.execute('SELECT border,name FROM %s' % city)
#         area_list = c.fetchall()

#     conn = sqlite3.connect('LianJia_area.db')
#     cursor = conn.cursor()
#     try:
#         sql = '''create table %s (
#                         id int PRIMARY KEY ,
#                         district text,
#                         name text,
#                         longitude text,
#                         latitude text,
#                         unit_price int,
#                         count int
#                         )
#             ''' % city
#         cursor.execute(sql)
#     except:
#         pass
#     for x in area_list:
#         lat = []
#         lng = []
#         district = x[1]
#         for y in x[0].split(';'):
#             lng.append(float(y.split(',')[0]))
#             lat.append(float(y.split(',')[1]))
#         li = []
#         step = 0.02
#         for x in numpy.arange(min(lng), max(lng), step):
#             for y in numpy.arange(min(lat), max(lat), step):
#                 li.append((round(y, 6), round(y - step, 6), round(x, 6), round(x - step, 6)))
#         pbar = tqdm.tqdm(li)
#         for x in pbar:

#             ret = Lianjia(city).GetCommunityInfo(x[0], x[1], x[2], x[3])

#             if ret is not None:
#                 for z in ret:
#                     try:
#                         sql = ''' insert into %s
#                                  (id, name, district,longitude,latitude,unit_price,count)
#                                  values
#                                  (:id, :name, :district,:longitude, :latitude, :unit_price, :count)
#                                  ''' % city
#                         z.update({'district': district})
#                         cursor.execute(sql, z)
#                         conn.commit()

#                         pbar.set_description(district + z['name'] + '已导入')
#                     except:

#                         pbar.set_description(district + z['name'] + '住房已存在')


def GetCommunityInfo(city_id, max_lat, min_lat, max_lng, min_lng) -> list:

    """
    :str max_lat:
    最大经度 六位小数str型max_lat='40.074766'

    :str min_lat:
    最小经度 六位小数str型min_lat='39.609408'

    :str max_lng:
    最大纬度 六位小数str型max_lng='40.074766'

    :str min_lng:
    最小纬度 六位小数str型min_lng='39.609408'

    :str city_id:
    北京:110000  上海:310000


    #获取区域内在售小区的信息#例如上海市的陈湾小区ID地理位置平均价格在售套数

    :return: list

    [{'id': '5011000012693', 'name': '陈湾小区', 'longitude': 121.455211, 'latitude': 30.966981, 'unit_price': 24407, 'count': 9}]


    """
    agnet = Agnet()

    time_13 = int(round(time.time() * 1000))
    authorization = agnet.GetAuthorization(
        {'group_type': 'community', 'city_id': city_id, 'max_lat': max_lat, 'min_lat': min_lat,
            'max_lng': max_lng, 'min_lng': min_lng, 'request_ts': time_13})

    url = agnet.url % (
        city_id, 'community', max_lat, min_lat, max_lng, min_lng, '%7B%7D', time_13, authorization, time_13)

    with requests.Session() as sess:
        ret = sess.get(url=url, headers=agnet.headers, cookies=agnet.cookies)
        # 将接收到的结果保存到文件
        with open(SAVE_PATH, 'w') as f:
            f.write(ret.text)

        # house_json = json.loads(ret.text[43:-1])

        # if house_json['errno'] == 0:
        #     data_list = []
        #     if type(house_json['data']['list']) is dict:
        #         for x in house_json['data']['list']:
        #             data_list.append(house_json['data']['list'][x])
        #         return data_list
        #     else:
        #         return house_json['data']['list']

        # else:
        #     return None

# def HoleCityDown(city):  # 爬取小区套数平均价格
#     with sqlite3.connect('district.db') as conn:
#         c = conn.cursor()
#         c.execute('SELECT border,name FROM %s' % city)
#         area_list = c.fetchall()

#     conn = sqlite3.connect('LianJia_area.db')
#     cursor = conn.cursor()
#     try:
#         sql = '''create table %s (
#                         id int PRIMARY KEY ,
#                         district text,
#                         name text,
#                         longitude text,
#                         latitude text,
#                         unit_price int,
#                         count int
#                         )
#             ''' % city
#         cursor.execute(sql)
#     except:
#         pass
#     for x in area_list:
#         lat = []
#         lng = []
#         district = x[1]
#         for y in x[0].split(';'):
#             lng.append(float(y.split(',')[0]))
#             lat.append(float(y.split(',')[1]))
#         li = []
#         step = 0.02
#         for x in numpy.arange(min(lng), max(lng), step):
#             for y in numpy.arange(min(lat), max(lat), step):
#                 li.append((round(y, 6), round(y - step, 6), round(x, 6), round(x - step, 6)))
#         pbar = tqdm.tqdm(li)
#         for x in pbar:

#             ret = Lianjia(city).GetCommunityInfo(x[0], x[1], x[2], x[3])

#             if ret is not None:
#                 for z in ret:
#                     try:
#                         sql = ''' insert into %s
#                                  (id, name, district,longitude,latitude,unit_price,count)
#                                  values
#                                  (:id, :name, :district,:longitude, :latitude, :unit_price, :count)
#                                  ''' % city
#                         z.update({'district': district})
#                         cursor.execute(sql, z)
#                         conn.commit()

#                         pbar.set_description(district + z['name'] + '已导入')
#                     except:

#                         pbar.set_description(district + z['name'] + '住房已存在')

if __name__ == '__main__':
    df = pd.read_csv(PATH1)
    # 打印第一行数据
    # print(df.head(2))

    num = 1

    print("request data: ", df['city_id'][num], df['max_lat'][num], df['min_lat'][num], df['max_lng'][num], df['min_lng'][num])

    # 以第一行数据为例 请求数据
    GetCommunityInfo(
        str(df['city_id'][num]),
        str(df['max_lat'][num]),
        str(df['min_lat'][num]),
        str(df['max_lng'][num]),
        str(df['min_lng'][num])
    )