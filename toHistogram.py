import json
import matplotlib.pyplot as plt

if __name__ == '__main__':
    json_path = './dataset/json/5.json'
    # 读取JSON文件
    with open(json_path, 'r') as file:
        json_data = file.read()

    # 解析JSON数据
    data = json.loads(json_data)
    areaList = []
    for index in range(len(data) - 1):
        areaList.append(data[index]['area'])

    print(areaList)
    print(len(areaList))

    # 统计个数
    count_dict = {}

    # 确定区间间隔
    min_value, max_value = min(areaList), max(areaList)
    start_pre = (min_value // 100) * 100
    end_pre = (max_value // 100) * 100
    for i in range(end_pre // 100 - start_pre // 100 + 1):
        range_label = f'[{start_pre + i * 100},{start_pre + (i + 1) * 100})'
        count_dict[range_label] = 0

    for num in areaList:
        range_start = (num // 100) * 100
        range_end = range_start + 100
        range_label = f'[{range_start},{range_end})'
        count_dict[range_label] += 1


    # 提取区间和对应的个数
    ranges = list(count_dict.keys())
    counts = list(count_dict.values())

    plt.bar(range(len(counts)), counts, align='center')
    # plt.xticks(range(len(counts)), ranges)
    plt.xticks(range(len(counts)), ranges, rotation=45)  # 旋转45度，

    plt.xlabel('Range')
    plt.ylabel('Count')
    plt.title('Element Count by Range')
    plt.tight_layout()  # 自动调整图像布局
    # plt.show()
    plt.savefig(f'./dataset/histogram/{json_path[15:-5]}.png')






















