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
    # 创建视频剪辑
    clip = ImageSequenceClip(images, fps=fps)
    # 写出为视频文件
    clip.write_videofile(out_path, codec='libx264')


if __name__ == '__main__':
    folder_paths = ["./data/0004/0004_img/", "./data/0004_gt/", "./data/0004_prediction/"]
    out_paths = ["./data/0004/0004.mp4", "./data/0004_gt/0004_gt.mp4", "./data/0004_prediction/0004_prediction.mp4"]

    for folder_path, out_path in zip(folder_paths, out_paths):
        image_files = [img for img in os.listdir(folder_path) if img.endswith((".png", ".jpg", ".jpeg"))]
        # 按文件名排序
        image_files.sort()
        images = [cv2.imread(os.path.join(folder_path, img)) for img in image_files]

        join_video(images, out_path)
