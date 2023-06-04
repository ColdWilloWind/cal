import json
from PIL import Image
import numpy as np


def bfs(image_array, row : int, col : int):
    """
    输入起始坐标(row, col),返回该白色区域的像素个数 cnt，像素坐标范围[min_row, max_row, min_col, max_col]
    :param image_array: 二值图像数组
    :param row: 横坐标
    :param col: 纵坐标
    :return: cnt, [min_row, max_row, min_col, max_col]
    """
    q = [(row, col)]  # 队列
    pos = 0
    cnt = 0

    min_row = 255
    max_row = 0
    min_col = 255
    max_col = 0

    image_array[row][col] = 0   # 标记开始节点已被访问
    while not pos == len(q):    # 队列非空
        # 出队
        (i, j) = q[pos]
        pos += 1
        # 当前节点 面积、像素个数加一
        cnt += 1
        # 求像素范围
        if i < min_row:
            min_row = i
        if i > max_row:
            max_row = i
        if j < min_col:
            min_col = j
        if j > max_col:
            max_col = j
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

    return cnt, [min_row, max_row, min_col, max_col]


def load_image_info(image_path):
    """

    :param image_path: 图片地址
    :return: cnt_graph: 白色区域的个数\n
    int,\n
    image_info：每个白色区域的像素个数和位置信息\n
    [{"area": area, "position": position}, ......]
    """
    # 打开二值图像
    image = Image.open(image_path)

    # 将图像转换为NumPy数组
    image_array = np.array(image)

    # 连通图个数
    cnt_graph = 0

    # 连通图信息： 面积大小（像素个数）、位置信息
    image_info = []

    for i in range(256):
        for j in range(256):
            if image_array[i][j] == 255:
                cnt_graph += 1
                area, position = bfs(image_array, i, j)
                info = {"area": area, "position": position}
                image_info.append(info)

    return cnt_graph, image_info


# 输入图片，将变化区域数量，变化区域像素点个数和位置信息导出到json文件
if __name__ == '__main__':

    image_path = './dataset/image/5.png'

    cnt = load_image_info(image_path)

    print(cnt)



