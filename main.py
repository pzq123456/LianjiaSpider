from lianjia import SaveCityBorderIntoDB, HoleCityDown
from city_dict import get_city_list

import pandas as pd
import tqdm

import time
import random

# 随机休眠时间
def random_sleep(min_time=1, max_time=5, variation_factor=1.5):
    """
    模拟人类行为的随机休眠时间
    :param min_time: 最小休眠时间，默认1秒
    :param max_time: 最大休眠时间，默认5秒
    :param variation_factor: 控制休眠时间的波动幅度，默认1.5倍
    :return: 实际休眠时间
    """
    # 生成随机的休眠时间，并加入一些变化
    sleep_time = random.uniform(min_time, max_time) * random.uniform(1, variation_factor)
    time.sleep(sleep_time)
    return round(sleep_time, 2)

# 休眠时间的模拟人类操作
def random_think(min_time=0.5, max_time=2):
    """
    模拟思考、处理的短暂停顿
    """
    sleep_time = random.uniform(min_time, max_time)
    time.sleep(sleep_time)
    return round(sleep_time, 2)

if __name__ == '__main__':
    city_list = get_city_list()  # 获取城市列表
    print(city_list[0])
    SaveCityBorderIntoDB(city_list[0])  # 下载城市区域数据

    # # tqdm 进度条循环显示城市名称
    # for city in tqdm.tqdm(city_list, desc="正在处理城市数据"):
    #     tqdm.tqdm.write(f"开始处理城市: {city}")

    #     try:
    #         # 模拟人类的短暂思考/延迟
    #         think_time = random_think()
    #         tqdm.tqdm.write(f"模拟思考 {think_time} 秒")

    #         SaveCityBorderIntoDB(city)  # 下载城市区域数据

    #         # 在下载数据间加入短暂停顿
    #         think_time = random_think()
    #         tqdm.tqdm.write(f"模拟短暂停顿 {think_time} 秒")

    #     except Exception as e:
    #         tqdm.tqdm.write(f"遇到错误: {e}")
    #         continue

    #     # 模拟随机休眠，休眠时间较长
    #     sleep_time = random_sleep(10, 60, variation_factor=2)  # 10-60秒的休眠，并有一定随机波动
    #     tqdm.tqdm.write(f"休眠 {sleep_time} 秒")

    #             # HoleCityDown(city)  # 下载区域住房数据
    
    # # 下载区域住房数据
    # for city in tqdm.tqdm(city_list, desc="正在处理城市数据"):
    #     tqdm.tqdm.write(f"开始处理城市: {city}")

    #     try:
    #         # 模拟人类的短暂思考/延迟
    #         think_time = random_think()
    #         tqdm.tqdm.write(f"模拟思考 {think_time} 秒")

    #         HoleCityDown(city)  # 下载区域住房数据

    #         # 在下载数据间加入短暂停顿
    #         think_time = random_think()
    #         tqdm.tqdm.write(f"模拟短暂停顿 {think_time} 秒")

    #     except Exception as e:
    #         tqdm.tqdm.write(f"遇到错误: {e}")
    #         continue

    #     # 模拟随机休眠，休眠时间较长
    #     sleep_time = random_sleep(10, 60, variation_factor=2)  # 10-60秒的休眠，并有一定随机波动
    #     tqdm.tqdm.write(f"休眠 {sleep_time} 秒")
    
    # tqdm.tqdm.write("全部城市数据处理完成！")

