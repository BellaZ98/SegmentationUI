# -*- coding: utf-8 -*-
"""
@Project    : SegUI
@File       : UI_slider.py
@Author     : Bella
@CreateTime : 2024/4/30 下午2:55
"""
import time

import gradio as gr
import cv2
import numpy as np
import os
import random


def find_file(video_path, folder_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    # 在指定文件夹中寻找匹配的 Ground Truth 文件
    for file in os.listdir(folder_path):
        if file.startswith(base_name):
            return os.path.join(folder_path, file)
    return None  # 如果没有找到匹配的文件，则返回 None


def extract_frames(video_path):
    """从视频中提取帧并保存为图片列表"""
    cap = cv2.VideoCapture(video_path)
    frames = []
    success, image = cap.read()
    frame_count = 0
    while success:
        rgb_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # 将图像从 BGR 转换为 RGB
        frame_count += 1
        frames.append(rgb_image)
        success, image = cap.read()
    cap.release()
    return frames, frame_count


def display_frame(frames, frame_index):
    """显示指定索引的帧"""
    frame = frames[int(frame_index - 1)]
    time.sleep(0.6 + random.random() * 0.3)  # 模拟模型处理时间
    return frame


def process_video(video_path, frame_index):
    frames, total_frames = extract_frames(video_path)
    folder_paths = ["data/0004_prediction", "data/0004_gt", "data/0004_masked_prediction", "data/0004_masked_gt"]
    video_paths = [find_file(video_path, folder_path) for folder_path in folder_paths]
    frames_list = [frames] + [extract_frames(video_path)[0] for video_path in video_paths]
    return [display_frame(frames, frame_index) for frames in frames_list]


def main():

    with gr.Blocks() as demo:
        gr.Markdown("# 医学影像分割（视频单帧查看）")
        gr.Markdown("上传一个医学影像视频，查看分割结果和 Ground Truth。")
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 上传视频")
                video_input = gr.Video(label="上传视频")
                # if video_input is None:
                #     _, total_frames = extract_frames(video_input)
                # else:
                #     total_frames = 2
                total_frames = 30  # gradio目前的版本还不支持动态更改其中控件的属性，这里为了创建帧数滚动条，先指定总帧数为30，后面看看怎么改比较好
                frame_slider = gr.Slider(minimum=1, maximum=total_frames, label="选择帧", step=1)
            with gr.Column():
                gr.Markdown("### 预测结果")
                image_output2 = gr.Image(show_label=False)
            with gr.Column():
                gr.Markdown("### 基于预测结果mask的原图")
                image_output4 = gr.Image(show_label=False)

        with gr.Row():
            with gr.Column():
                gr.Markdown("### 原视频帧")
                image_output1 = gr.Image(show_label=False)
            with gr.Column():
                gr.Markdown("### Ground Truth")
                image_output3 = gr.Image(show_label=False)
            with gr.Column():
                gr.Markdown("### 基于预测结果mask的ground truth")
                image_output5 = gr.Image(show_label=False)

        frame_slider.change(fn=process_video,
                            inputs=[video_input, frame_slider],
                            outputs=[image_output1, image_output2, image_output3, image_output4, image_output5])

    demo.launch()


if __name__ == "__main__":
    main()
