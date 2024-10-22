import hashlib
import random
import time
import requests
import os
import json
import pandas as pd

PATH = os.path.dirname(os.path.abspath(__file__))
PATH1 = os.path.join(PATH, 'data', 'district_bounds.csv')

SAVE_PATH = os.path.join(PATH, 'result', 'test.txt')

proxies = {
    'http': 'http://localhost:7890',
    'https': 'http://localhost:7890'
}

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

    return agent

class Agnet():
    def __init__(self) -> None:
        # https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId={cityId}&dataSource={dataSource}&condition={condition}&id={id}&groupType={groupType}&maxLatitude={maxLatitude}&minLatitude={minLatitude}&maxLongitude={maxLongitude}&minLongitude={minLongitude}
        self.url = 'https://map.ke.com/proxyApi/i.c-pc-webapi.ke.com/map/bubblelist?cityId=%s&dataSource=%s&maxLatitude=%s&minLatitude=%s&maxLongitude=%s&minLongitude=%s&groupType=%s&request_ts=%s'
        
        self.header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'map.ke.com',
            'Origin': 'https://map.lianjia.com',
            'plat': 'LJ',
            'Referer': 'https://map.lianjia.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': ua()
        }

        self.agent = ua()
    
    def getTimestamp(self):
        return int(round(time.time() * 1000))

    def getURL(self, city_id, max_lat, min_lat, max_lng, min_lng):
        return self.url % (city_id, 'ESF', max_lat, min_lat, max_lng, min_lng, 'community', self.getTimestamp())


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def save_json(file_path, data):
    # 保存为 utf-8 格式
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_json(json_data):
    # 根据 data "totalCount" 字段
    totalCount = json_data['data']['totalCount']

    if totalCount == 0:
        # 报错
        raise Exception('No data found')
    else:
        # 解析数据
        return json_paser(json_data['data']["bubbleList"])

def json_paser(data):
    pass
    # "bubbleList": [
    # {
    #     "fullSpell": "c1111027375552",
    #     "desc": "5.9万(106套)",
    #     "count": 106,
    #     "countStr": "106套",
    #     "countUnit": "套",
    #     "price": "58933",
    #     "priceStr": "5.9万",
    #     "priceUnit": "元",
    #     "border": "116.449769,39.874743;116.449603,39.874082;116.449594,39.873462;116.451701,39.873407;116.451678,39.873961;116.450825,39.874708",
    #     "bubbleDesc": "10AM新坐标",
    #     "icon": "",
    #     "entityId": "1111027375552",
    #     "entityType": "resblock",
    #     "id": 1111027375552,
    #     "name": "10AM新坐标",
    #     "longitude": 116.45053,
    #     "latitude": 39.874376,
    #     "imageType": 30002,
    #     "selected": false
    # },

def get_grids(max_lat, min_lat, max_lng, min_lng, step=0.1):
    # 生成网格 从左上角开始
    grids = []
    for i in range(int((max_lat - min_lat) / step) + 1):
        for j in range(int((max_lng - min_lng) / step) + 1):
            lat1 = max_lat - i * step       # 左上角纬度
            lat2 = max_lat - (i + 1) * step # 左下角纬度
            lng1 = min_lng + j * step       # 左上角经度
            lng2 = min_lng + (j + 1) * step # 右上角经度
            grids.append([lat1, lat2, lng1, lng2])
    return grids

if __name__ == '__main__':
    df = pd.read_csv(PATH1)
    # 打印第一行数据
    # print(df.head(2))
    agent = Agnet()

    # 生成网格
    # grids = get_grids(df['max_lat'][0], df['min_lat'][0], df['max_lng'][0], df['min_lng'][0])
    # print(len(grids))

    # for grid in grids:
    #     # print(grid)
    #     request_url = agent.getURL(df['city_id'][0], grid[0], grid[1], grid[2], grid[3])
    #     print(request_url)

    request_url = agent.getURL(df['city_id'][0], df['max_lat'][0], df['min_lat'][0], df['max_lng'][0], df['min_lng'][0])
    print(request_url)
    # response = requests.get(request_url, headers=agent.header, proxies=proxies)
    # save the response
    # with open(SAVE_PATH, 'w') as f:
    #     f.write(response.text)

    # json_data = load_json(SAVE_PATH)
    # print(json_data)
    # save_json(SAVE_PATH, json_data)


