import os
from PIL import Image
from coordinate import load_image_info
import matplotlib.pyplot as plt


def load_images_from_folder(folder):
    """

    :param folder: 文件夹地址
    :return: folder中的所有 .png 文件
    """
    image_list = []
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            img = Image.open(os.path.join(folder, filename))
            image_list.append(img)
    return image_list


def print_bar_image(cnt_dict):
    """
    输入 y_label(像素个数在对应区间的白色区域数量), x_label（单个白色区域的像素个数区间（0， 65536]）绘制的柱状图
    :param cnt_dict: [{'(start_area, end_area]': value}, ......]
    :return: 对应的柱状图
    """
    # 提取区间和对应的个数
    ranges = list(cnt_dict.keys())
    counts = list(cnt_dict.values())

    plt.bar(range(len(counts)), counts, align='center')
    # plt.xticks(range(len(counts)), ranges)
    plt.xticks(range(len(counts)), ranges, rotation=45)  # 旋转45度，

    plt.xlabel('Area Range')
    plt.ylabel('Change Region Count')
    # plt.title('Element Count by Range')
    plt.tight_layout()  # 自动调整图像布局
    plt.show()
    # plt.savefig(f'./dataset/histogram/{json_path[15:-5]}.png')


def divide_pixel_ranges(min_value, max_value, num_intervals):
    interval_width = (max_value - min_value) // num_intervals

    interval_boundaries = []

    for i in range(1, num_intervals):
        boundary = min_value + (i * interval_width)
        interval_boundaries.append(boundary)

    interval_boundaries.append(max_value)

    return interval_boundaries


def count_values_in_ranges(values, ranges):
    result = dict.fromkeys(ranges, 0)  # 初始化结果字典，值都为0

    for value in values:
        for key in ranges:
            range_str = key.strip('(]')  # 去除括号
            start, end = map(int, range_str.split(','))  # 将区间字符串转换为起始值和结束值
            if start < value <= end:
                result[key] += 1
                break  # 如果找到了对应的区间，就不需要再继续比较后面的区间了

    return result


if __name__ == '__main__':
    # 指定包含图像文件的文件夹路径
    # whu 7k+, levir-cd 400+
    whu_cd_path = '/mnt/E/dataset/CD_dataset/WHU/label'
    levir_cd_path = '/mnt/E/dataset/LEVIR-CD/train/label'

    # 读取所有图片的绝对地址, 调用函数加载图像到列表中
    images = []
    images.extend(load_images_from_folder(whu_cd_path))
    images.extend(load_images_from_folder(levir_cd_path))

    # 打印列表中的图像数量
    print("Loaded", len(images), "images.")

    # 计算所有的图片的变化区域之和
    cnt = 0
    change_region_area_list = []
    for image in images:
        cnt_graph, image_infos = load_image_info(image)
        cnt += cnt_graph
        for image_info in image_infos:
            change_region_area_list.append(image_info['area'])

    # 统计个数
    count_dict = {'(0,656]': 0, '(656,16384]': 0, '(16384,65536]': 0}

    # 确定间隔区间 (0,656] (656,16384] (16384,65536]
    for num in change_region_area_list:
        if num <= 656:
            count_dict['(0,656]'] += 1
        elif 656 < num <= 16384:
            count_dict['(656,16384]'] += 1
        else:
            count_dict['(16384,65536]'] += 1

    print_bar_image(count_dict)

    # 将(0, 656] 分成十份，统计其中的变化区域数量
    small_count_dict = {'(0,66]': 0, '(66,132]': 0, '(132,198]': 0, '(198,264]': 0, '(264,330]': 0,
                        '(330,396]': 0, '(396,462]': 0, '(462,528]': 0, '(528,594]': 0, '(594,656]': 0}

    small_count_dict = count_values_in_ranges(change_region_area_list, small_count_dict)

    print_bar_image(small_count_dict)


