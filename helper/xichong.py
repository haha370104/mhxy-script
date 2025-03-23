from helper.image import get_game_screen, find_img_position, target_window, transform_PIL_to_cv2
from helper.mouse import find_img_click
from helper.ocr import ocr
import cv2
import time
from functools import reduce

def move_to_c66():
    find_img_click('picture\\c66.png')

def confirm():
    find_img_click('picture\\confirm_xilian.png')

def get_zizhi_rect():
    base_rect = target_window.rect
    xilian_window_position = find_img_position('picture\\xilian_title.png')
    x = xilian_window_position[0] - 255 - base_rect[0]
    y = xilian_window_position[1] + 175 - base_rect[1]
    screen = get_game_screen()
    zizhi_rect = screen.crop((x, y, x + 222, y + 85))

    result_list = []
    width = 111
    height = 20
    for x in range(2):
        for y in range(4):
            base_x = x * width
            base_y = y * height
            num_rect = zizhi_rect.crop((base_x + 60 + x * 15, base_y, base_x + width, base_y + height))
            _, binary_img = cv2.threshold(transform_PIL_to_cv2(num_rect), 175, 255, cv2.THRESH_BINARY_INV)
            result_list.append(binary_img)
    [attack_img, defend_img, health_img, _, magic_img, speed_img, dodge_img, growth_img] = result_list

    return {
        'attack': attack_img,
        'defend': defend_img,
        'health': health_img,
        'magic': magic_img,
        'speed': speed_img,
        'dodge': dodge_img,
        'growth': growth_img
    }

def parse_zizhi():
    zizhi_img_dict = get_zizhi_rect()
    result = {}

    for key in zizhi_img_dict.keys():
        ocr_result = ocr.ocr_for_single_line(zizhi_img_dict[key])
        if ocr_result['score'] < 0.85:
            print('识别有危险', ocr_result)
            input('请确认')
        result[key] = float(ocr_result['text'].replace(' ', ''))

    return result

def run_xichong(times):
    max_sum = 0
    max_growth = 0

    print('准备完毕，1秒后开始')
    time.sleep(1)
    print('开始')

    for i in range(times):
        print('\n')
        print('第' + str(i + 1) + '次洗宠')

        zizhi_dict = parse_zizhi()

        growth = zizhi_dict['growth']
        zizhi_sum = reduce(lambda x, y: x + y, zizhi_dict.values()) - growth

        max_sum = max(max_sum, zizhi_sum)
        max_growth = max(max_growth, growth)

        print('攻 法', zizhi_dict['attack'], zizhi_dict['magic'])
        print('防 速', zizhi_dict['defend'], zizhi_dict['speed'])
        print('体 躲', zizhi_dict['health'], zizhi_dict['dodge'])
        print('成长:', growth, max_growth, '总资质:', zizhi_sum, max_sum)

        if growth >= 13:
            break
        if zizhi_sum > 65000:
            break
        if zizhi_sum > 55000 and zizhi_dict['attack'] > 10000 and zizhi_dict['speed'] > 8000:
            break
        # if zizhi_dict['attack'] > 8000 or zizhi_dict['speed'] > 8000:
        #     break

        move_to_c66()
        confirm()
        time.sleep(1)
