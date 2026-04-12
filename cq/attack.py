from time import sleep

from ascript.windows.action import mouse_move
from ascript.windows.screen import find_images
from datetime import datetime, timedelta
import win32gui
import win32con
import os

from helper.capture import capture_window_by_hwnd, bring_window_to_foreground
from ascript.windows import window

def random_teleport(hwnd):
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_NUMPAD4, 0)
    sleep(0.5)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_NUMPAD4, 0)

def check_is_attacking(hwnd, check_times=10, threshold=4):
    save_path = os.path.join(os.getcwd(), 'screen_main.png')

    match_times = 0

    for _ in range(check_times):
        img = capture_window_by_hwnd(hwnd)
        img.save(save_path)
        try:
            match_result = find_images(os.path.join(os.path.dirname(__file__), '..\\picture\\cq\\attack_result.png'), source_file=save_path, confidence=0.8, res_num=0)
        except Exception as e:
            match_result = []

        current_match_times = len(match_result)
        match_times = max(current_match_times, match_times)
        print('本次匹配数', current_match_times, match_times)
        if match_times >= threshold:
            return True
        sleep(0.2)

    print('检测', match_times)
    return match_times >= threshold

def check_is_too_far(hwnd):
    save_path = os.path.join(os.getcwd(), 'screen_main.png')
    img = capture_window_by_hwnd(hwnd)
    img.save(save_path)
    try:
        match_result = find_images(os.path.join(os.path.dirname(__file__), '..\\picture\\cq\\too_far_alert.png'), source_file=save_path, confidence=0.7, res_num=0)
        return len(match_result) > 0
    except Exception as e:
        return False

def check_empty_mp(hwnd):
    save_path = os.path.join(os.getcwd(), 'screen_main.png')
    img = capture_window_by_hwnd(hwnd)
    img.save(save_path)
    try:
        match_result = find_images(os.path.join(os.path.dirname(__file__), '..\\picture\\cq\\empty_mp.png'), source_file=save_path, confidence=0.5, res_num=0)
        return len(match_result) > 0
    except Exception as e:
        return False

def main():
    while True:
        all_windows = window.find_all()

        target_window = None
        chrome_window = None

        for item in all_windows:
            if 'Google Chrome' in item.title:
                chrome_window = item

        sleep_time = 15

        for item in all_windows:
            if item.title == '健奇3' and item.name == 'WindowsForms10.Window.8.app.0.2804c64_r8_ad1':

                if item.height < 800:
                    continue
                target_window = item
                break
        if check_is_too_far(target_window.hwnd):
            bring_window_to_foreground(hwnd=target_window.hwnd)
            x, y, x2, y2 = win32gui.GetWindowRect(target_window.hwnd)
            mouse_move((x2+x)/2, (y2+y)/2)
            bring_window_to_foreground(chrome_window.hwnd)

        # if check_empty_mp(target_window.hwnd):
        #     sleep_time=100

        try:
            if not check_is_attacking(target_window.hwnd):
                print('随机传送')
                random_teleport(target_window.hwnd)
                sleep_time = 1
        except Exception as e:
            random_teleport(target_window.hwnd)
        target_time = datetime.now() + timedelta(seconds=sleep_time)
        print('运行，下次执行时间', target_time.strftime('%Y-%m-%d %H:%M:%S'))
        sleep(sleep_time)


main()
