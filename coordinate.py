import os
import json
import numpy as np
from PIL import Image
from tqdm import tqdm
from utils import load_images_from_folder


def get_folder_addresses(directory):
    folder_addresses = []
    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            folder_addresses.append(os.path.join(root, folder))
    return folder_addresses


def bfs(image_array, row : int, col : int):
    """
    输入起始坐标(row, col),返回该白色区域的像素个数 cnt
    :param image_array: 二值图像数组 256 × 256
    :param row: 横坐标
    :param col: 纵坐标
    :return: cnt
    """
    q = [(row, col)]  # 队列
    pos = 0
    change_region_area = 0

    image_array[row][col] = 0   # 标记开始节点已被访问
    while not pos == len(q):    # 队列非空
        # 出队
        (i, j) = q[pos]
        pos += 1
        # 当前节点 面积、像素个数加一
        change_region_area += 1
        # 访问周围的八个邻居坐标
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if x == i and y == j:
                    continue  # 跳过中心坐标

                # 检查坐标是否超出边界
                if x < 0 or x > 255 or y < 0 or y > 255:
                    continue  # 跳过超出边界的坐标

                if image_array[x][y] == 255:
                    image_array[x][y] = 0   # 标记邻居节点已访问
                    q.append((x, y))        # 加入队列

    return change_region_area


def load_image_info(image_path):
    """

    :param image_path: 图片地址
    :return: cnt_graph: 白色区域的个数\n
    int,\n
    image_info：每个白色区域的像素个数和位置信息\n
    [{"area": area, "position": position}, ......]
    image_mode : 确定图像的类型（RGB或L）
    """
    # 打开二值图像
    original_image = Image.open(image_path)
    image_mode = original_image.mode

    # 将图像转换为灰度图像
    if original_image.mode != 'L':
        grayscale_image = original_image.convert('L')
    else:
        grayscale_image = original_image

    # 将图像转换为NumPy数组
    image_array = np.array(grayscale_image)

    # 连通图个数
    cnt_graph = 0

    # 连通图信息： 面积大小（像素个数）、位置信息
    image_info = []

    for i in range(256):
        for j in range(256):
            if image_array[i][j] == 255:
                cnt_graph += 1
                area = bfs(image_array, i, j)
                info = {"area": area, "position": (i, j)}
                image_info.append(info)

    return cnt_graph, image_info, image_mode


# 输入图片，将变化区域数量，变化区域像素点个数和位置信息导出到json文件
if __name__ == '__main__':

    levir_path = './dataset/levir/'

    # levir_path = '/mnt/D/liushuangze/label/LEVIR/'
    folder_list = get_folder_addresses(levir_path)

    print(folder_list)

    for one_folder in tqdm(folder_list, desc='Processing'):
        folder_name = os.path.basename(one_folder)
        folder_info = []
        image_list = load_images_from_folder(one_folder)
        for image_path in image_list:
            cnt_graph, area_info, image_mode = load_image_info(image_path)
            image_info = {'image_path': image_path, 'image_mode': image_mode,
                          'count': cnt_graph, 'areaList': area_info}
            folder_info.append(image_info)

        json_data = json.dumps(folder_info, indent=4)
        json_file_path = f'./res/levir_json/{folder_name}.json'
        # 将 JSON 数据写入文件
        with open(json_file_path, 'w') as file:
            file.write(json_data)








