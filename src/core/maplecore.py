from .image_engine import get_hwnd_screen_buffer

import numpy as np
import time
import win32gui
import cv2
import keyboard
import mouse

trade_ui = cv2.imread('./src/resources/ui/trade.jpg', 0)
name_char = cv2.imread('./src/resources/char/name.png', 0)
medal_char = cv2.imread('./src/resources/char/medal.png', 0)

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
        self.mob_list = []
        self.lastest_detection_screen = None
        self.debug_mode = False

        l = get_window_list(caption)

        if len(l) > id:
            self.hWnd = l[id][1]
        
    def add_buff_key(self, img, key, delay=3):
        self.buff_key_list.append((cv2.imread(img, 0), key, delay))

    def activate_window(self):
        win32gui.SetForegroundWindow(self.hWnd)
    
    def add_reward_item(self, img):
        self.reward_list.append(cv2.imread(img, 0))
    
    def add_mob(self, img):
        self.mob_list.append(cv2.imread(img, 0))

    def get_game_screen(self):
        img = get_hwnd_screen_buffer(self.hWnd, self.scale)
        
        converted = np.array(img)
        src = cv2.cvtColor(converted, cv2.COLOR_BGR2RGB)
        src = cv2.flip(src, 0)
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        
        self.lastest_detection_screen = src

        return (src, gray)
    
    def get_detected_img(self, gray, img, threshold):
        w, h = img.shape[::-1]
        res = cv2.matchTemplate(gray, img, cv2.TM_CCOEFF_NORMED)

        loc = np.where( res >= threshold)

        return list(zip(*loc[::-1]))

        # cv2.rectangle(src, pt, (pt[0] + w, pt[1] + h), (0, 0,255), 2)

    def progress(self):
        src, gray = self.get_game_screen()

        for buff in self.buff_key_list:
            loc = self.get_detected_img(gray, buff[0], 0.7)

            if len(loc) == 0:
                keyboard.press(buff[1])
                time.sleep(buff[2])

        if self.debug_mode:
            pass
    
    def move_to_fm(self, gray):
        self.activate_window()

        loc = self.get_detected_img(gray, trade_ui, 0.9)

        mouse.move(loc[0][0] + 10, loc[0][1] + 10)
        mouse.click()
        
    def progress_sell_items(self):
        self.move_to_fm()
        time.sleep(2)
        keyboard.press('space')
    
    def get_name_location(self, gray):
        
        loc = self.get_detected_img(gray, medal_char, 0.9)

        if len(loc) == 0:
            return (0, 0)
            
        return (loc[0][0], loc[0][1])
        


        



    


