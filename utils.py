# -*- coding: utf-8 -*-
"""
@Project    : SegUI
@File       : utils.py
@Author     : Bella
@CreateTime : 2024/4/29 下午8:11
"""
import cv2
import os
from moviepy.editor import ImageSequenceClip
import numpy as np


def separate_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames


def join_video(images, out_path, fps=15):
    # 对于每个图像，将其转换为RGB格式
    rgb_images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]
    # 创建视频剪辑
    clip = ImageSequenceClip(rgb_images, fps=fps)
    # 写出为视频文件
    clip.write_videofile(out_path, codec='libx264')


def apply_translucent_mask(image, mask, color=None, alpha=0.3):
    """
    在输入图像上应用一个半透明的红色遮罩层。
    :param image: 输入的图像，应为BGR格式。
    :param mask: 分割mask，非零处表示遮罩应用的位置。
    :param color: 遮罩层的颜色，默认为红色。
    :param alpha: 遮罩层的透明度，默认为0.3。
    :return: 带有红色半透明遮罩层的图像。
    """
    # 确保mask是布尔型数组
    if color is None:
        color = [0, 0, 255]
    mask = mask.astype(bool)

    # 创建一个与输入图像同样大小的红色图层
    to_mask = np.zeros_like(image)
    to_mask[mask] = color

    # 将红色遮罩层叠加到原始图像上
    # cv2.addWeighted用于按指定的权重合并两个图像
    # 参数1：第一个图像，参数2：第一个图像的权重，参数3：第二个图像，参数4：第二个图像的权重，参数5：gamma值，这里设置为0
    output = cv2.addWeighted(image, 1, to_mask, alpha, 0)  # 透明度为30%

    return output


def process_masks(folder_a, folder_b, folder_c, color=None, alpha=0.3):
    # 确保输出文件夹存在
    if color is None:
        color = [0, 0, 255]
    os.makedirs(folder_c, exist_ok=True)

    # 遍历文件夹A中的所有图片
    for image_filename in os.listdir(folder_a):
        image_path = os.path.join(folder_a, image_filename)
        image_base, image_ext = os.path.splitext(image_filename)

        # 去除前两个字符并移除扩展名
        if len(image_base) > 2:
            part_of_name = image_base[2:]

            # 在文件夹B中查找包含part_of_name的文件
            mask_filename = next((f for f in os.listdir(folder_b) if part_of_name in os.path.splitext(f)[0]), None)
            if mask_filename:
                mask_path = os.path.join(folder_b, mask_filename)

                # 加载图像和mask
                image = cv2.imread(image_path)
                mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

                # 如果图像和mask都成功加载
                if image is not None and mask is not None:
                    result_image = apply_translucent_mask(image, mask, color, alpha)
                    save_path = os.path.join(folder_c, image_filename)
                    cv2.imwrite(save_path, result_image)
                    print(f"Processed and saved: {save_path}")
                else:
                    print(f"Failed to load image or mask for: {image_filename}")
            else:
                print(f"No matching mask found for: {image_filename}, skipping...")
        else:
            print(f"Filename '{image_filename}' is too short to process correctly, skipping...")


if __name__ == '__main__':
    # 使用示例
    process_masks('data/0004/0004_img/', 'data/0004_prediction/', 'data/0004_masked_prediction/')
    process_masks('data/0004/0004_img/', 'data/0004_gt/', 'data/0004_masked_gt/')
    # process_masks('data/0004/0004_img/', 'data/0004_gt/', 'data/0004_masked_gt/', color=[255, 0, 0], alpha=0.3)  #
    # # gt用蓝色标记

    folder_paths = ["./data/0004/0004_img/", "./data/0004_gt/", "./data/0004_prediction/", "./data/0004_masked_gt/",
                    "./data/0004_masked_prediction/"]
    out_paths = ["./data/0004/0004.mp4", "./data/0004_gt/0004_gt.mp4", "./data/0004_prediction/0004_prediction.mp4",
                 "./data/0004_masked_gt/0004_masked_gt.mp4", "./data/0004_masked_prediction/0004_masked_prediction.mp4"]

    for folder_path, out_path in zip(folder_paths, out_paths):
        image_files = [img for img in os.listdir(folder_path) if img.endswith((".png", ".jpg", ".jpeg"))]
        # 按文件名排序
        image_files.sort()
        images = [cv2.imread(os.path.join(folder_path, img)) for img in image_files]

        join_video(images, out_path)
