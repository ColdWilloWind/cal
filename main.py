# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# 根据生成的json文件可视化位置框
if __name__ == '__main__':

    # 读取二值图像
    image = plt.imread('./dataset/image/2.png')
    # 读取JSON文件
    with open('./dataset/json/2.json', 'r') as file:
        json_data = file.read()

    # 解析JSON数据
    data = json.loads(json_data)

    # 打印解析后的数据
    # print(data)
    for index in range(len(data) - 1):
        min_row, max_row, min_col, max_col = data[index]['position']
        rectangle = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, linewidth=2,
                                      edgecolor='r',
                                      facecolor='none')

        # 创建图像和轴
        fig, ax = plt.subplots()

        # 显示图像
        ax.imshow(image, cmap='gray')

        # 添加矩形框到轴
        ax.add_patch(rectangle)

        # 关闭坐标轴
        ax.axis('off')

        # 显示可视化结果
        plt.show()

