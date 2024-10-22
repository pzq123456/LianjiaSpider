import time
import pandas as pd
import os
import tqdm
import random
from log import get_logger, save_checkpoint

def random_sleep(min_time=1, max_time=5):
    """随机休眠一段时间
    Args:
        min_time (int, optional): _description_. Defaults to 1.
        max_time (int, optional): _description_. Defaults to 60.
    """
    sleeptime = random.uniform(min_time, max_time)
    time.sleep(sleeptime)
    return sleeptime

def generate_district_files(csv_path, base_path, logger, content_generator=None):
    # 默认内容生成方法
    if content_generator is None:
        content_generator = default_content_generator

    # 读取 CSV 数据
    df = pd.read_csv(csv_path)
    df = df.head(20)  # 仅保留前20行
    os.makedirs(base_path, exist_ok=True)

    for city in tqdm.tqdm(df['city_name'].unique(), desc="Processing"):
        
        city_path = os.path.join(base_path, city)
        os.makedirs(city_path, exist_ok=True)

        # 过滤出该城市的所有区
        city_districts = df[df['city_name'] == city]

        for index, row in tqdm.tqdm(city_districts.iterrows(), total=len(city_districts), desc=f"Processing {city}"):
            
            try:
                district_file = os.path.join(city_path, f"{row['district_name']}.csv")
                content_generator(row, district_file)

                logger.info(f"Processed {row['district_name']} in {city}")
                save_checkpoint(f"{city}-{row['district_name']}-{index}", 'success')
                sleep_time = random_sleep()
                logger.info(f"Sleeping for {sleep_time:.2f} seconds")

            except Exception as e:
                # print(f"Error processing {row['district_name']} in {city}: {e}")
                logger.error(f"Error processing {row['district_name']} in {city}: {e}")
                save_checkpoint(f"{city}-{row['district_name']}-{index}", 'failed')
                sleep_time = random_sleep()
                logger.info(f"Sleeping for {sleep_time:.2f} seconds")

def default_content_generator(row,save_path):
    # 有一定概率生成错误的内容
    if random.random() < 0.1:
        raise Exception("Random error")
    else:
        with open(save_path, 'w') as f:
            f.write(f"City: {row['city_name']}, District: {row['district_name']}")

# 使用示例
if __name__ == "__main__":
    PATH = os.path.join(os.path.dirname(__file__))
    PATH1 = os.path.join(PATH, 'data', 'district_bounds.csv')
    BASE_PATH = os.path.join(PATH, 'result')

    logger = get_logger()
    
    generate_district_files(PATH1, BASE_PATH, logger)
