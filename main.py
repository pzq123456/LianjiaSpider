import json
import os
import random
import pandas as pd
import requests
from log import get_logger
from manager import generate_district_files
from sipder import Agnet, process_json

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:  # 指定编码为 utf-8
        return json.load(f)

def ping_pong():
    # 请求某一个网址 以确定是否存在网络连接
    try:
        response = requests.get('https://www.baidu.com')
        if response.status_code == 200:
            return True
    except:
        return False

if __name__ == "__main__":
    PATH = os.path.join(os.path.dirname(__file__))
    PATH1 = os.path.join(PATH, 'data', 'district_bounds.csv')
    BASE_PATH = os.path.join(PATH, 'result')
    
    SAVE_PATH = os.path.join(PATH, 'result', 'test.txt')

    logger = get_logger()
    
    # generate_district_files(PATH1, BASE_PATH, logger)

    df = pd.read_csv(PATH1)

    agent = Agnet()

    def default_content_generator(row, save_path):
        
        # if not ping_pong():
        #     raise Exception("No network connection")
        # return

        request_url = agent.getURL(row['city_id'], row['max_lat'], row['min_lat'], row['max_lng'], row['min_lng'])
        response = requests.get(request_url, headers=agent.headers)
        data = response.json()
        # print(data)
        result = process_json(data)
        result.to_csv(save_path, index=False)

    generate_district_files(PATH1, BASE_PATH, logger, default_content_generator)
