from ascript.windows.screen import find_images, capture
from ascript.windows import window
import os
import numpy as np
import cv2

all_windows = window.find_all()

target_window = None
for item in all_windows:
    if '番茄花园[358]' in item.title:
        target_window = item

game_handler = target_window.hwnd


def get_game_screen():
    screen = capture(game_handler)
    return screen


def find_img_position(img_name: str):
    image_path = os.path.join(os.path.dirname(__file__), '..\\', img_name)
    result = find_images(image_path, confidence=0.5, res_num=0)
    first_match_point = result[0]['result']
    return first_match_point

def transform_PIL_to_cv2(img):
    # 将PIL图像转换为NumPy数组
    numpy_array = np.array(img)

    # 将颜色通道从RGB转换为BGR
    cv2_image = cv2.cvtColor(numpy_array, cv2.COLOR_RGB2BGR)

    return cv2_image
