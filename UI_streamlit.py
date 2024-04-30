# -*- coding: utf-8 -*-
"""
@Project    : SegUI
@File       : UI_streamlit.py
@Author     : Bella
@CreateTime : 2024/4/30 下午1:31
"""

import streamlit as st
import os
import subprocess
import sys
from io import BytesIO


def find_file(video_name, folder_name):
    base_name = os.path.splitext(video_name)[0]
    folder_path = os.path.join(os.path.dirname(__file__), folder_name)
    for file in os.listdir(folder_path):
        if file.startswith(base_name):
            return os.path.join(folder_path, file)
    return None


def main():
    st.title("医学影像分割")
    video_file = st.file_uploader("上传视频", type=["mp4", "avi"])

    if video_file is not None:
        video_bytes = BytesIO(video_file.read())  # Read the video file into a BytesIO object
        video_name = video_file.name

        predicted_video_path = find_file(video_name, "data/0004_prediction")
        ground_truth_video_path = find_file(video_name, "data/0004_gt")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.video(video_bytes)
        with col2:
            if predicted_video_path:
                st.video(predicted_video_path)
        with col3:
            if ground_truth_video_path:
                st.video(ground_truth_video_path)

        # JavaScript for synchronizing videos
        st.markdown("""
            <script>
                const videos = document.querySelectorAll('video');
                videos.forEach(vid => {
                    vid.onplay = (event) => {
                        let currentTime = event.target.currentTime;
                        videos.forEach(v => {
                            if (v != event.target) {
                                v.currentTime = currentTime;
                                v.play();
                            }
                        });
                    };
                    vid.onpause = (event) => {
                        videos.forEach(v => {
                            if (v != event.target) {
                                v.pause();
                            }
                        });
                    };
                });
            </script>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
