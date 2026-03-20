from time import sleep
from ascript.windows.action import mouse_move, click
from datetime import datetime, timedelta
import win32gui
import win32con
import os

from helper.image import get_game_screen, find_img_position
from helper.mouse import find_img_click
from helper.capture import capture_window_by_hwnd, bring_window_to_foreground
from ascript.windows import window

all_windows = window.find_all()

def check_handler_is_mining(handler, file_path):
    hwnd_screen = capture_window_by_hwnd(handler)
    hwnd_screen.save(file_path)

def repair(hwnd):
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, 50, 0)
    sleep(0.5)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, 50, 0)

def sell_all(offset_x, offset_y, source):
    select_all_position = find_img_position('picture\\cq\\select_all.png', source=source)
    mouse_move(select_all_position[0]+offset_x, select_all_position[1]+offset_y, duration=0.3)
    click(button='left')
    sleep(1)
    sell_position = find_img_position('picture\\cq\\sell.png', source=source)
    mouse_move(sell_position[0]+offset_x, sell_position[1]+offset_y, duration=0.3)
    click(button='left')
    sleep(1)

def main():
    while True:
        for item in all_windows:
            if item.title == '健奇3' and item.name == 'WindowsForms10.Window.8.app.0.2804c64_r8_ad1':
                save_path = os.path.join(os.getcwd(), 'screen.png')
                check_handler_is_mining(item.hwnd, save_path)
                print(item)

                try:
                    find_img_position('picture\\cq\\user_name.png', source=save_path)
                    bring_window_to_foreground(item.hwnd)
                    print(item)
                    repair(item.hwnd)
                    sell_all(item.rect[0], item.rect[1], save_path)
                except Exception as e:
                    raise e
                    continue
        sleep_time = 1800
        target_time = datetime.now() + timedelta(seconds=sleep_time)
        print('运行，下次执行时间', target_time.strftime('%Y-%m-%d %H:%M:%S'))
        sleep(sleep_time)

main()
