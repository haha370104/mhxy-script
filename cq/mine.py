from time import sleep
from ascript.windows.action import mouse_move, click
from datetime import datetime, timedelta
import win32gui
import win32con
import os

from helper.image import get_game_screen, find_img_position
from helper.capture import capture_window_by_hwnd, bring_window_to_foreground
from ascript.windows import window

def check_handler_is_mining(handler, file_path):
    hwnd_screen = capture_window_by_hwnd(handler)
    hwnd_screen.save(file_path)

def repair(hwnd):
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, 50, 0)
    sleep(0.5)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, 50, 0)

def sell_all(offset_x, offset_y, source):
    select_all_position = find_img_position('picture\\cq\\select_all_button.png', source=source)
    mouse_move(select_all_position[0]+offset_x, select_all_position[1]+offset_y, duration=0)
    click(button='left')
    sleep(0.1)
    sell_position = find_img_position('picture\\cq\\sell.png', source=source)
    mouse_move(sell_position[0]+offset_x, sell_position[1]+offset_y, duration=0)
    click(button='left')

def main():
    while True:
        all_windows = window.find_all()

        chrome_window = None

        for item in all_windows:
            if 'Google Chrome' in item.title:
                chrome_window = item
        for item in all_windows:
            if item.title == '健奇3' and item.name == 'WindowsForms10.Window.8.app.0.2804c64_r8_ad1':
                if item.height > 800:
                    continue

                save_path = os.path.join(os.getcwd(), 'screen.png')
                check_handler_is_mining(item.hwnd, save_path)

                try:
                    find_img_position('picture\\cq\\user_name.png', source=save_path)
                    bring_window_to_foreground(item.hwnd)
                    repair(item.hwnd)
                    rect = win32gui.GetWindowRect(item.hwnd)
                    sell_all(rect[0], rect[1], save_path)
                except Exception as e:
                    continue
                finally:
                    bring_window_to_foreground(chrome_window.hwnd)
                    sleep(1)
        sleep_time = 2000
        target_time = datetime.now() + timedelta(seconds=sleep_time)
        print('运行，下次执行时间', target_time.strftime('%Y-%m-%d %H:%M:%S'))
        sleep(sleep_time)

main()
