import win32gui
import win32ui
from PIL import Image
import ctypes
import win32con
import win32process
import win32api
import time

def capture_window_by_hwnd(hwnd):
    """
    通过窗口句柄捕获窗口截图（后台操作，无需前台）
    :param hwnd: 目标窗口句柄
    :return: PIL.Image 对象（截图），失败返回 None
    """
    # 1. 验证窗口句柄有效性
    if not win32gui.IsWindow(hwnd):
        print(f"错误：无效的窗口句柄 {hwnd}")
        return None

    # 2. 获取窗口客户区的大小（不含标题栏/边框，PrintWindow默认捕获客户区）
    # 若要捕获整个窗口（含标题栏），改用 win32gui.GetWindowRect
    rect = win32gui.GetClientRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    if width <= 0 or height <= 0:
        bring_window_to_foreground(hwnd)
        return capture_window_by_hwnd(hwnd)

    # 3. 创建内存DC和位图，用于接收窗口图像
    # 获取窗口的DC
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    # 创建内存DC（兼容DC）
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    # 创建内存兼容DC
    save_dc = mfc_dc.CreateCompatibleDC()
    # 创建位图对象（大小匹配窗口）
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    # 将位图选入内存DC
    save_dc.SelectObject(save_bitmap)

    # 4. 核心：调用PrintWindow捕获窗口图像
    # PW_RENDERFULLCONTENT：Windows 8+ 支持，确保捕获完整内容（解决部分窗口黑块问题）
    PW_RENDERFULLCONTENT = 0x00000002
    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)
    if result == 0:
        print("警告：PrintWindow调用失败，尝试降级捕获")
        # 降级方案：无PW_RENDERFULLCONTENT参数
        result = win32gui.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)
        if result == 0:
            print("错误：PrintWindow彻底失败")
            # 释放资源
            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            return None

    # 5. 将位图转换为PIL Image对象
    # 获取位图数据
    bmp_info = save_bitmap.GetInfo()
    bmp_str = save_bitmap.GetBitmapBits(True)
    # 转换为PIL图像（注意格式：BGR → RGB）
    img = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str,
        'raw',
        'BGRX',
        0,
        1
    )

    # 6. 释放所有Windows GDI资源（必须释放，否则内存泄漏）
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return img


def bring_window_to_foreground(hwnd):
    """
    将指定句柄的窗口调到前台（处理最小化、权限、无响应等问题）
    :param hwnd: 目标窗口句柄（整数）
    :return: 成功返回True，失败返回False
    """
    # 步骤1：验证窗口句柄是否有效
    if not win32gui.IsWindow(hwnd):
        print(f"错误：句柄 {hwnd} 不是有效窗口")
        return False

    # 步骤2：如果窗口最小化，先还原
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.1)  # 等待窗口还原（必须加短延迟）

    # 步骤3：解决“SetForegroundWindow权限不足”问题（关键）
    # 原理：附加到目标窗口的线程输入，提升焦点优先级
    current_thread_id = win32api.GetCurrentThreadId()
    target_thread_id = win32process.GetWindowThreadProcessId(hwnd)[0]
    # 附加线程输入（临时共享输入状态）
    if current_thread_id != target_thread_id:
        win32process.AttachThreadInput(current_thread_id, target_thread_id, True)

    try:
        # 步骤4：强制将窗口调到前台
        win32gui.SetForegroundWindow(hwnd)
        # 步骤5：激活窗口（确保输入焦点）
        win32gui.SetActiveWindow(hwnd)
        # 步骤6：可选：将窗口设为正常大小（避免最大化/最小化异常）
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

        # 验证：检查窗口是否真的在前台
        foreground_hwnd = win32gui.GetForegroundWindow()
        if foreground_hwnd == hwnd:
            print(f"成功：窗口 {hwnd} 已调到前台")
            return True
        else:
            print(f"失败：窗口 {hwnd} 未成为前台窗口（当前前台：{foreground_hwnd}）")
            return False
    except Exception as e:
        print(f"：调前台失败{e}")
        return False
    finally:
        # 步骤7：解除线程输入附加（避免内存泄漏）
        if current_thread_id != target_thread_id:
            win32process.AttachThreadInput(current_thread_id, target_thread_id, False)