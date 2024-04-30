# -*- coding: utf-8 -*-
"""
@Project    : SegmentationUI
@File       : UI_sin_image.py
@Author     : Bella
@CreateTime : 2024/5/1 上午4:34
"""

import os
import cv2
import numpy as np
import random
import gradio as gr
from pathlib import Path


def find_file(video_path, folder_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    # 在指定文件夹中寻找匹配的 Ground Truth 文件
    for file in os.listdir(folder_path):
        if file.startswith(base_name):
            return os.path.join(folder_path, file)
    return None  # 如果没有找到匹配的文件，则返回 None


def find_matching_file(file_path_A, folder_B):
    # 使用 Path 获取文件名和扩展名
    file_name = Path(file_path_A).stem
    search_pattern = file_name[2:]  # 从第三个字符开始，不包含扩展名

    # 遍历 folder_B 中的所有文件
    for file in os.listdir(folder_B):
        # 检查文件名中是否包含指定的子字符串
        if search_pattern in Path(file).stem:
            # 如果找到，返回完整的文件路径
            return os.path.join(folder_B, file)
    # 如果没有找到匹配的文件，返回 None
    return None


def process_image(image_path, folder_paths=None):
    if folder_paths is None:
        folder_paths = ["./data/0004/0004_img/", "./data/0004_gt/", "./data/0004_prediction/", "./data/0004_masked_gt/",
                        "./data/0004_masked_prediction/"]
    image_paths = [find_matching_file(image_path, folder_path) for folder_path in folder_paths]
    return [cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB) for image_path in image_paths]


def main():
    with gr.Blocks() as demo:
        gr.Markdown("# 医学影像分割（单张图片）")
        gr.Markdown("上传一个医学影像图片，查看分割结果和 Ground Truth。")
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 上传图片")
                file_input = gr.File(label="上传图片", file_types=["png", "jpg", "jpeg"])
                image_output1 = gr.Image(show_label=False)
                submit_button = gr.Button("Submit")
            with gr.Column():
                gr.Markdown("### 预测结果")
                image_output2 = gr.Image(show_label=False)
                gr.Markdown("### Ground Truth")
                image_output3 = gr.Image(show_label=False)
            with gr.Column():
                gr.Markdown("### 基于预测结果mask的原图")
                image_output4 = gr.Image(show_label=False)
                gr.Markdown("### 基于预测结果mask的ground truth")
                image_output5 = gr.Image(show_label=False)

        submit_button.click(fn=process_image,
                            inputs=file_input,
                            outputs=[image_output1, image_output2, image_output3, image_output4, image_output5])

    demo.launch()


if __name__ == "__main__":
    main()
