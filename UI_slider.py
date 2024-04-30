# -*- coding: utf-8 -*-
"""
@Project    : SegUI
@File       : UI_slider.py
@Author     : Bella
@CreateTime : 2024/4/30 下午2:55
"""

import gradio as gr
import cv2
import numpy as np
import os


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
    return frame


def main():
    video_path = "data/0004/0004.mp4"  # 需要指定视频路径
    frames, total_frames = extract_frames(video_path)

    with gr.Blocks() as demo:
        gr.Markdown("# 视频帧选择器")
        frame_slider = gr.Slider(minimum=0, maximum=total_frames - 1, label="选择帧")
        image_output = gr.Image()

        frame_slider.change(fn=lambda frame_index: display_frame(frames, frame_index), inputs=frame_slider,
                            outputs=image_output)

    demo.launch()


if __name__ == "__main__":
    main()
