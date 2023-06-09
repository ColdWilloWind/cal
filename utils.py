import os
import json
import numpy as np
from PIL import Image


def image_to_numpy(image_path):
    # 打开二值图像
    original_image = Image.open(image_path)

    # 将图像转换为灰度图像
    if original_image.mode != 'L':
        grayscale_image = original_image.convert('L')
    else:
        grayscale_image = original_image

    # 将图像转换为NumPy数组
    image_array = np.array(grayscale_image)

    return image_array


def bfs(image_array, row: int, col: int):
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

    image_array[row][col] = 0  # 标记开始节点已被访问
    while not pos == len(q):  # 队列非空
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
                    image_array[x][y] = 0  # 标记邻居节点已访问
                    q.append((x, y))  # 加入队列

    return change_region_area


def load_image_info(image_path):
    """

    :param image_path: 图片地址
    :return: cnt_graph: 白色区域的个数\n
    int,\n
    image_info：每个白色区域的像素个数和位置信息\n
    [{"area": area, "position": position}, ......]
    """

    # 将图像转换为NumPy数组
    image_array = image_to_numpy(image_path)

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

    return cnt_graph, image_info


def load_image_info(image_path):
    """

    :param image_path: 图片地址
    :return: cnt_graph: 白色区域的个数\n
    int,\n
    image_info：每个白色区域的像素个数和位置信息\n
    [{"area": area, "position": position}, ......]
    """
    # 打开二值图像
    original_image = Image.open(image_path)

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

    return cnt_graph, image_info


def load_images_from_folder(folder):
    """

    :param folder: 文件夹地址
    :return: folder中的所有 .png 文件
    """
    image_list = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = os.path.join(folder, filename)
            image_list.append(img)
    return image_list


def load_and_print_json(file_path='./res/levir_json/BIT.json'):
    # 从 JSON 文件中加载数据
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # 遍历加载的数据
    for item in json_data:
        image_path = item['image_path']
        count = item['count']
        areaList = item['areaList']

        print("图像路径:", image_path)
        print("计数:", count)
        print("区域列表:")
        for area in areaList:
            area_value = area['area']
            position = area['position']
            print("- 区域:", area_value)
            print("· 位置:", position)
        print()


def load_and_process_json(file_path, pixel_threshold):
    """
    根据图片信息的json文件，按照pixel_threshold
    :param file_path:  json文件地址
    :param pixel_threshold: 像素面积阈值
    :return:
    """
    # 从 JSON 文件中加载数据
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    output_dir = './res/levir'

    # 遍历加载的数据
    for item in json_data:
        image_path = item['image_path']
        image_array = image_to_numpy(image_path)
        areaList = item['areaList']
        for area in areaList:
            area_value = area['area']
            if area_value > pixel_threshold:
                position = area['position']
                image_array = process_image(image_array, position)

        # 图片（./dataset/levir/BIT\1.png）上级目录 （BIT）
        image_parent_dir = os.path.basename(os.path.dirname(image_path))
        # ./res/levir/BIT/132/
        if not os.path.exists(os.path.join(output_dir, image_parent_dir, str(pixel_threshold))):
            # 创建目录
            os.makedirs(os.path.join(output_dir, image_parent_dir, str(pixel_threshold)))

        new_image_path = os.path.join(output_dir, image_parent_dir, str(pixel_threshold), os.path.basename(image_path))
        im = Image.fromarray(image_array)
        im.save(new_image_path)


def process_image(image_array, pixel_coordinate):
    """
    处理单个区域，根据坐标（pixel_coordinate），将image_array中的白色区域变黑
    :param image_array:
    :param pixel_coordinate:
    :return:
    """
    # 复制原始图像，以便进行处理
    processed_image = np.copy(image_array)

    # 根据像素坐标对图像进行处理
    row, col = pixel_coordinate
    # 进行处理的操作...
    # 例如，可以将指定像素设置为特定值或根据其周围像素进行修改。
    q = [(row, col)]  # 队列
    pos = 0

    processed_image[row][col] = 0  # 标记开始节点已被访问
    while not pos == len(q):  # 队列非空
        # 出队
        (i, j) = q[pos]
        pos += 1
        # 访问周围的八个邻居坐标
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if x == i and y == j:
                    continue  # 跳过中心坐标

                # 检查坐标是否超出边界
                if x < 0 or x > 255 or y < 0 or y > 255:
                    continue  # 跳过超出边界的坐标

                if processed_image[x][y] == 255:
                    processed_image[x][y] = 0  # 标记邻居节点已访问
                    q.append((x, y))  # 加入队列

    # 返回处理后的二值图像
    return processed_image


if __name__ == '__main__':
    load_and_print_json()
