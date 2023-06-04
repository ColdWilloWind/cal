import cv2

# 计算变化区域数量
if __name__ == '__main__':
    # 读取标签图像
    label_image = cv2.imread('./dataset/image/3.png', cv2.IMREAD_GRAYSCALE)  # 替换为你的标签图像路径

    # 使用连通组件标记算法进行标记
    _, labeled_image = cv2.connectedComponents(label_image)

    # 统计连通组件的数量（白色区域的数量）
    white_regions = labeled_image.max()  # labeled_image中最大的标记值即为连通组件的数量

    print("白色区域的数量:", white_regions)