import numpy as np
from PIL import Image


def compress_png_image(image_path):
    # 打开原始图像
    original_image = Image.open(image_path)

    # 将图像转换为灰度图像
    grayscale_image = original_image.convert('L')

    # 将灰度图像转换为NumPy数组
    grayscale_array = np.array(grayscale_image)

    # 创建一个形状为（256，256）的空白图像
    compressed_array = np.zeros((256, 256), dtype=np.uint8)

    # 设置新图像的像素值
    compressed_array[grayscale_array == 255] = 255

    return compressed_array


def create_rgb_image(image_name = '1'):
    # 创建一个形状为（256，256，3）的空白图像
    image_array = np.zeros((256, 256, 3), dtype=np.uint8)

    # 设置所有像素值为（0，0，0）
    image_array[:, :, :] = [0, 0, 0]
    image_array[0, 0, :] = [255, 255, 255]

    # 将NumPy数组转换为PIL图像对象
    image = Image.fromarray(image_array)

    # 保存图像
    image.save(f'./dataset/whu/{image_name}.png')


if __name__ == '__main__':
    create_rgb_image()
    array = compress_png_image('./dataset/whu/1.png')
    print(array)