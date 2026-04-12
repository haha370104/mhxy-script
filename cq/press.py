from time import sleep
import win32gui
import win32con
from ascript.windows import window

def main():
    while True:
        all_windows = window.find_all()

        target_window = None

        for item in all_windows:
            if item.title == '健奇3' and item.name == 'WindowsForms10.Window.8.app.0.2804c64_r8_ad1':

                if item.height < 800:
                    continue
                target_window = item
                break

        win32gui.SendMessage(target_window.hwnd, win32con.WM_KEYDOWN, win32con.VK_NUMPAD3, 0)
        sleep(0.1)
        win32gui.SendMessage(target_window.hwnd, win32con.WM_KEYUP, win32con.VK_NUMPAD3, 0)

main()
