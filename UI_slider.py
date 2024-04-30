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
        frame_count += 1
        frames.append(image)
        success, image = cap.read()
    cap.release()
    return frames, frame_count


def display_frame(frames, frame_index):
    """显示指定索引的帧"""
    frame = frames[int(frame_index)]
    time.sleep(1 + random.random() * 0.3)
    return frame


def main():
    input_path = "data/0004/0004.mp4"  # 需要指定视频路径
    _, total_frames = extract_frames(input_path)
    folder_paths = ["data/0004_prediction", "data/0004_gt", "data/0004_masked_prediction", "data/0004_masked_gt"]
    video_paths = [find_file(input_path, folder_path) for folder_path in folder_paths]
    frames_list = [extract_frames(input_path)[0]] + [extract_frames(video_path)[0] for video_path in video_paths]

    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                gr.Markdown("# 上传视频")
                frame_slider = gr.Slider(minimum=0, maximum=total_frames - 1, label="选择帧")
                image_output1 = gr.Image()

            with gr.Column():
                gr.Markdown("# 预测结果")
                image_output2 = gr.Image()
                gr.Markdown("# ground truth")
                image_output3 = gr.Image()

            with gr.Column():
                gr.Markdown("# 基于预测结果mask的原图")
                image_output4 = gr.Image()
                gr.Markdown("# 基于预测结果mask的ground truth")
                image_output5 = gr.Image()

            frame_slider.change(fn=lambda frame_index: [display_frame(frames, frame_index) for frames in frames_list],
                                inputs=frame_slider,
                                outputs=[image_output1, image_output2, image_output3, image_output4, image_output5])

    demo.launch()


if __name__ == "__main__":
    main()
