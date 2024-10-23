import pandas as pd
import json
import os

PATH = os.path.dirname(os.path.abspath(__file__))

SAVE_PATH = os.path.join(PATH, 'result', 'test.txt')

def json_parser(data):
    # 将 bubbleList 转换为 DataFrame
    df = pd.DataFrame(data)
    return df
    
    # 保存为 CSV 文件
    # df.to_csv('output.csv', index=False)

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:  # 指定编码为 utf-8
        return json.load(f)
# 调用解析函数
# json_parser(data)

if __name__ == '__main__':
    data = load_json(SAVE_PATH)
    json_parser(data['data']['bubbleList']) # 取前 10 条数据
