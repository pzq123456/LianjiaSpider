import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import os 

PATH = os.path.dirname(os.path.abspath(__file__))
PATH1 = os.path.join(PATH,"data","cn_city.geojson")

SAVED_PATH1 = os.path.join(PATH,"data","city_bounds.csv")
SAVED_PATH2 = os.path.join(PATH,"data","city_dict.txt")

# 保存为字典 能直接被python读取
def save_dict(city_dict):
    with open(SAVED_PATH2, "w") as f:
        f.write(str(city_dict))

def read_dict(path):
    with open(path, "r") as f:
        city_dict = eval(f.read())
    return city_dict

def get_city_list():
    # 读取城市边界数据
    # pd
    df = pd.read_csv(SAVED_PATH1)
    city_list = df["city_name"].tolist()
    return city_list

def process_geojson_to_dict_and_csv(geojson_file, csv_output, dict_output):
    """
    处理GeoJSON数据并提取城市信息，返回字典格式，同时导出为CSV文件。
    
    :param geojson_file: 输入的GeoJSON文件路径
    :param csv_output: 输出的CSV文件路径
    :return: 包含城市信息的字典
    """
    # 读取GeoJSON文件
    gdf = gpd.read_file(geojson_file)

    # 初始化存储结果的字典和列表
    city_dict = {}
    csv_data = []

    # 使用tqdm添加进度条
    for _, row in tqdm(gdf.iterrows(), total=len(gdf), desc="Processing cities"):
        # print(row)
        # 获取城市名称和省份代码
        # city_name = row["properties"]["ct_name"]
        # pr_adcode = row["properties"]["pr_adcode"]
        city_name = row["ct_name"]
        pr_adcode = row["pr_adcode"]

        # 提取几何体 (geometry) 并计算边界
        bounds = row.geometry.bounds
        min_lng, min_lat, max_lng, max_lat = bounds

        # 构建字典项
        city_dict[city_name] = {
            'city_id': pr_adcode,
            'max_lat': max_lat,
            'min_lat': min_lat,
            'max_lng': max_lng,
            'min_lng': min_lng
        }

        # 添加到CSV数据列表
        csv_data.append({
            'city_name': city_name,
            'city_id': pr_adcode,
            'max_lat': max_lat,
            'min_lat': min_lat,
            'max_lng': max_lng,
            'min_lng': min_lng
        })
        # break

    # 将结果转换为DataFrame并保存为CSV
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_output, index=False)

    # 保存为字典
    save_dict(city_dict)

    return city_dict

def get_whole_cn_city_dict():
    # if not os.path.exists(SAVED_PATH2):
        # process_geojson_to_dict_and_csv(PATH1, SAVED_PATH1, SAVED_PATH2)
    city_dict = read_dict(SAVED_PATH2)
    return city_dict


if __name__ == "__main__":
    process_geojson_to_dict_and_csv(PATH1, SAVED_PATH1, SAVED_PATH2)
    # city_dict = read_dict(SAVED_PATH2)
    # print(city_dict)
