from .image_engine import get_hwnd_screen_buffer

import numpy as np
import win32gui
import cv2

def get_window_list(text):
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)

        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title == text:
            hwnd_list.append((title, hwnd))

        return True
    
    output = []
    win32gui.EnumWindows(callback, output)
    return output


class MapleCore:

    def __init__(self, caption, scale=1.0, id=0):
        self.hWnd = 0
        self.scale = scale
        self.buff_key_list = []
        self.reward_list = []
        self.lastest_detection_screen = None
        self.debug_mode = False

        l = get_window_list(caption)

        if len(l) > id:
            self.hWnd = l[id][1]
        
    def add_buff_key(self, img, key, delay=3000):
        self.buff_key_list.append((cv2.imread(img), key, delay))

    def activate_window(self):
        win32gui.SetForegroundWindow(self.hWnd)
    
    def add_reward_item(self, icon):
        self.reward_list.append(icon)
    
    def get_game_screen(self):
        win32gui.InvalidateRect()
        img = get_hwnd_screen_buffer(self.hWnd, self.scale)
        
        converted = np.array(img)
        src = cv2.cvtColor(converted, cv2.COLOR_BGR2RGB)
        src = cv2.flip(src, 0)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

        return (src, gray)
    
    def check_status(self):
        src, gray = self.get_game_screen()

        if self.debug_mode:
            src = 1

    


