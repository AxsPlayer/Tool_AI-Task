# -*- coding: utf-8 -*-
from PIL import Image
import sys


def fill_image(image):
    """
    对于不为正方形的图片，进行填充到正方形

    :param image:
    :return:
    """
    # 获取图片长宽
    width, height = image.size
    # 选取长和宽中较大值作为新图片的size
    new_image_length = width if width > height else height
    # 生成新图片[白底]
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
    # 将之前的图粘贴在新图上，居中
    if width > height:
        new_image.paste(image, (0, int((new_image_length - height) / 2)))  # (x,y)二元组表示粘贴上图相对下图的起始位置
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))

    return new_image


def cut_image(image):
    """
    切成九宫图

    :param image:
    :return:
    """
    # 获取图片size
    width, height = image.size
    item_width = int(width / 3)
    box_list = []

    # 按九宫格切图
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]

    return image_list

def save_images(image_name, image_list):
    """
    保存图片

    :param image_list:
    :return:
    """
    index = 1
    image_name = image_name.split('.')[0]
    for image in image_list:
        image.save(image_name + '_九宫格_' + str(index) + '.png', 'PNG')
        index += 1


def main_cut(image_name):
    """
    裁剪九宫格的主函数

    :param image_name:
    :return:
    """
    image = Image.open(image_name)
    image = fill_image(image)
    image_list = cut_image(image)
    save_images(image_name, image_list)
