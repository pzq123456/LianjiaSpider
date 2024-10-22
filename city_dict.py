import geopandas as gpd
import pandas as pd
from tqdm import tqdm
import os 

PATH = os.path.dirname(os.path.abspath(__file__))
PATH1 = os.path.join(PATH,"data","cn_city.geojson")
# data\district.geojson
PATH2 = os.path.join(PATH,"data","district.geojson")

SAVED_PATH1 = os.path.join(PATH,"data","city_bounds.csv")
SAVED_PATH2 = os.path.join(PATH,"data","city_dict.txt")
SAVED_PATH3 = os.path.join(PATH,"data","district_bounds.csv")
SAVED_PATH4 = os.path.join(PATH,"data","district_dict.txt")

# 保存为字典 能直接被python读取
def save_dict(city_dict):
    with open(SAVED_PATH2, "w") as f:
        f.write(str(city_dict))

def read_dict(path): 
    with open(path, "r", encoding="gbk") as f:
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

def process_district_to_dict_and_csv(geojson_file, csv_output, dict_output):
    '''
    处理GeoJSON数据并提取城市信息，返回字典格式，同时导出为CSV文件。
    '''
    # { "type": "Feature", "properties": 
    #  { "dt_adcode": "110101", "dt_name": "东城区", "ct_adcode": "110100", "ct_name": "北京城区", "pr_adcode": "110000", "pr_name": "北京市", "cn_adcode": "100000", "cn_name": "中华人民共和国" }, 
    #  "geometry": { "type": "MultiPolygon", "coordinates": []} 
    # }
    # 提取 "dt_adcode" "dt_name" "ct_name" 及 max_lat min_lat max_lng min_lng
    gdf = gpd.read_file(geojson_file)

    csv_data = []
    for _, row in tqdm(gdf.iterrows(), total=len(gdf), desc="Processing districts"):
        district_name = row["dt_name"]
        city_name = row["ct_name"]
        pr_adcode = row["pr_adcode"]
        bounds = row.geometry.bounds
        min_lng, min_lat, max_lng, max_lat = bounds
        csv_data.append({
            'district_name': district_name,
            'city_name': city_name,
            'city_id': pr_adcode,
            'max_lat': max_lat,
            'min_lat': min_lat,
            'max_lng': max_lng,
            'min_lng': min_lng
        })
    df = pd.DataFrame(csv_data)
    df.to_csv(csv_output, index=False)

    return district_dict


def get_whole_cn_city_dict():
    # if not os.path.exists(SAVED_PATH2):
        # process_geojson_to_dict_and_csv(PATH1, SAVED_PATH1, SAVED_PATH2)
    city_dict = read_dict(SAVED_PATH2)
    return city_dict


if __name__ == "__main__":
    # process_geojson_to_dict_and_csv(PATH1, SAVED_PATH1, SAVED_PATH2)
    # city_dict = read_dict(SAVED_PATH2)
    # print(city_dict)

    process_district_to_dict_and_csv(PATH2, SAVED_PATH3, SAVED_PATH4)
    district_dict = read_dict(SAVED_PATH4)
    print(district_dict[0])

