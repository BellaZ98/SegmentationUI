import gradio as gr
import numpy as np
from utils import separate_video, join_video
import time
import os
import random
# from your_segmentation_model import segment_frame


def find_file(video_path, folder_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    # 在指定文件夹中寻找匹配的 Ground Truth 文件
    for file in os.listdir(folder_path):
        if file.startswith(base_name):
            return os.path.join(folder_path, file)
    return None  # 如果没有找到匹配的文件，则返回 None


def process_video(video_path):
    # 读取视频
    # predictions = []
    #
    # frames = separate_video(video_path)
    #
    # # 将预测结果与原始帧合成视频
    # pred_path = 'output_video.avi'
    # out = cv2.VideoWriter(pred_path, cv2.VideoWriter_fourcc(*'DIVX'), 15, (frame.shape[1], frame.shape[0]))
    # for frame in frames:
    #     predictions.append(segment_frame(frame))
    #
    # for pred in predictions:
    # #     out.write(pred.astype('uint8'))  # 确保预测结果为正确的数据类型
    # out.release()

    # 加载预测视频
    pred_path = find_file(video_path, 'data/0004_prediction/')
    # 加载 ground truth 视频
    gt_path = find_file(video_path, 'data/0004_gt/')
    masked_pred_path = find_file(video_path, 'data/0004_masked_prediction/')
    masked_gt_path = find_file(video_path, 'data/0004_masked_gt')
    time.sleep(8 + random.random()*2)  # 模拟模型处理时间
    return pred_path, gt_path, masked_pred_path, masked_gt_path


with gr.Blocks() as demo:
    gr.Markdown("# 医学影像分割")
    gr.Markdown("上传一个医学影像视频，查看分割结果和 Ground Truth。")
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="上传视频")
            submit_button = gr.Button("Submit")
            gr.Markdown("### 上传视频")

        with gr.Column():
            video_output1 = gr.Video(label="预测结果")
            gr.Markdown("### 预测结果")
            video_output2 = gr.Video(label="Ground Truth(通过文件名匹配)")
            gr.Markdown("### Ground Truth(通过文件名匹配)")

        with gr.Column():
            video_output3 = gr.Video(label="经过预测结果masked后的原视频")
            gr.Markdown("### 经过预测结果masked后的原视频")
            video_output4 = gr.Video(label="经过Ground Truth masked后的原视频")
            gr.Markdown("### 经过Ground Truth masked后的原视频")

    submit_button.click(
        process_video,
        inputs=video_input,
        outputs=[video_output1, video_output2, video_output3, video_output4]
    )


demo.launch()
