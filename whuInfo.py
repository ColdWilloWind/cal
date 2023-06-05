import numpy as np
from PIL import Image
from statisticInfo import load_images_from_folder
from statisticInfo import print_bar_image
from statisticInfo import count_values_in_ranges


def compress_png_image(image_path):
    # 打开原始图像
    original_image = Image.open(image_path)

    # 将图像转换为灰度图像
    if original_image.mode != 'L':
        grayscale_image = original_image.convert('L')

    # 将灰度图像转换为NumPy数组
    grayscale_array = np.array(grayscale_image)

    # 创建一个形状为（256，256）的空白图像
    compressed_array = np.zeros((256, 256), dtype=np.uint8)

    # 设置新图像的像素值
    compressed_array[grayscale_array == 255] = 255

    return compressed_array


def whu_and_levir_bfs(image_array, row, col):
    q = [(row, col)]  # 队列
    pos = 0
    cnt = 0

    image_array[row][col] = 0  # 标记开始节点已被访问
    while not pos == len(q):  # 队列非空
        # 出队
        (i, j) = q[pos]
        pos += 1
        # 当前节点 面积、像素个数加一
        cnt += 1

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

    return cnt


def load_whu_and_levir_image(image_path):
    """

    :param image_path: 256 * 256 * 3 rgb png 图像地址
    :return: cnt_graph -> int： 该图像中白色区域数量
    image_info -> list[int, ...]： 每个白色区域的像素个数
    """
    # 打开二值图像
    # image = Image.open(image_path)

    # 将图像转换为NumPy数组
    image_array = compress_png_image(image_path)

    # 连通图个数
    cnt_graph = 0

    # 连通图信息： 面积大小（像素个数）
    image_info = []

    for i in range(256):
        for j in range(256):
            if image_array[i][j] == 255:
                cnt_graph += 1
                area = whu_and_levir_bfs(image_array, i, j)
                image_info.append(area)

    return cnt_graph, image_info


def area_distribution_by_three(areaList):
    # 统计个数
    count_dict = {'(0,656]': 0, '(656,16384]': 0, '(16384,65536]': 0}
    # 确定间隔区间 (0,656] (656,16384] (16384,65536]
    for num in areaList:
        if num <= 656:
            count_dict['(0,656]'] += 1
        elif 656 < num <= 16384:
            count_dict['(656,16384]'] += 1
        else:
            count_dict['(16384,65536]'] += 1

    return count_dict


def area_distribution_by_ten(areaList):
    # 将(0, 656] 分成十份，统计其中的变化区域数量
    small_count_dict = {'(0,66]': 0, '(66,132]': 0, '(132,198]': 0, '(198,264]': 0, '(264,330]': 0,
                        '(330,396]': 0, '(396,462]': 0, '(462,528]': 0, '(528,594]': 0, '(594,656]': 0}

    small_count_dict = count_values_in_ranges(areaList, small_count_dict)

    return small_count_dict


if __name__ == '__main__':

    whu_cd_path = '/mnt/E/dataset/CD_dataset/WHU/label'
    levir_cd_path = '/mnt/E/dataset/LEVIR-CD/cut_LEVIR_CD/label'
    images = []

    images.extend(load_images_from_folder(whu_cd_path))
    images.extend(load_images_from_folder(levir_cd_path))

    # 打印列表中的图像数量
    print("Loaded", len(images), "images.")

    # test
    # images = ['./dataset/whu/1.png']

    cnt = 0

    change_region_area_list = []

    for image in images:
        cnt_graph, image_infos = load_whu_and_levir_image(image)
        cnt += cnt_graph
        change_region_area_list.extend(image_infos)

    # print(cnt)
    # print(change_region_area_list)

    area_dict_three = area_distribution_by_three(change_region_area_list)
    print_bar_image(area_dict_three)

    area_dict_ten = area_distribution_by_ten(change_region_area_list)
    print_bar_image(area_dict_ten)


