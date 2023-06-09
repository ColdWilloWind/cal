import os
from tqdm import tqdm
from utils import load_and_process_json


if __name__ == '__main__':
    json_path = './res/levir_json'
    json_list = []

    threshold_list = [132, 264, 396, 528, 656]

    for root, dirs, files in os.walk(json_path):
        for file in files:
            json_list.append(os.path.join(json_path, file))

    # print(json_list)
    for file in tqdm(json_list, desc='Processing'):
        for threshold in threshold_list:
            load_and_process_json(file, threshold)
