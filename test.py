from statisticInfo import divide_pixel_ranges
from statisticInfo import count_values_in_ranges
from statisticInfo import print_bar_image
import matplotlib.pyplot as plt


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., height,
                    '%d' % int(height),
                    ha='center', va='bottom')

if __name__ == '__main__':
    # change_region_area_list = [33, 4, 123, 456, 10, 78, 356, 656]
    # small_count_dict = {'(0,66]': 9994, '(66,132]': 34545, '(132,198]': 3434, '(198,264]': 2223, '(264,330]': 20,
    #                     '(330,396]': 40, '(396,462]': 1000, '(462,528]': 6799, '(528,594]': 450, '(594,656]': 1}
    #
    # print_bar_image(small_count_dict)


    # 示例数据
    x = [1, 2, 3, 4, 5]
    y = [10, 7, 5, 3, 8]

    # 创建柱状图
    rects = plt.bar(x, y)

    # 标注数值
    autolabel(rects)

    # 显示图形
    plt.show()
