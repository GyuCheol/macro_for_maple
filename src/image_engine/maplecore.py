from PIL import ImageGrab

import numpy as np
import cv2

from win32 import win32gui
from win32.lib import win32con
from pythonwin import win32ui
from ctypes import wintypes
from PIL import Image

import ctypes

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD),
        ]

def getWindowList(text):
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

        l = getWindowList(caption)

        if len(l) > id:
            self.hWnd = l[id][1]
            position = win32gui.GetWindowRect(self.hWnd)
        
    def add_buff_key(self, img, key):
        self.buff_key_list.append((img, key))

    def activate_window(self):
        win32gui.SetForegroundWindow(self.hWnd)
    
    def set_window_size(self, height, width):

        cw = width
        ch = height

        win32gui.MoveWindow(self.hWnd, 0, 0, cw, ch, True)
        

    def get_window_screen(self):
        rect = win32gui.GetWindowRect(self.hWnd)

        width = int((rect[2] - rect[0]) * self.scale)
        height = int((rect[3] - rect[1]) * self.scale)

        device_context = win32gui.GetWindowDC(self.hWnd)
        compatible_dc = win32gui.CreateCompatibleDC(device_context)
        
        win32gui.SetStretchBltMode(compatible_dc, win32con.COLORONCOLOR)
        width = int(rect[2] * self.scale)
        height = int(rect[3] * self.scale)

        bitmap = win32gui.CreateCompatibleBitmap(device_context, width, height)
        bmp = win32gui.GetObject(bitmap)

        bi = BITMAPINFOHEADER()
        bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bi.biWidth = bmp.bmWidth
        bi.biHeight = bmp.bmHeight
        bi.biPlanes = bmp.bmPlanes
        bi.biBitCount = bmp.bmBitsPixel
        bi.biCompression = 0 # BI_RGB
        bi.biSizeImage = 0
        bi.biXPelsPerMeter = 0
        bi.biYPelsPerMeter = 0
        bi.biClrUsed = 0
        bi.biClrImportant = 0

        pixel = bmp.bmBitsPixel
        size = ((bmp.bmWidth * pixel + pixel - 1)//pixel) * 4 * bmp.bmHeight
        buf = (ctypes.c_char * size)()

        win32gui.SelectObject(compatible_dc, bitmap)

        win32gui.StretchBlt(compatible_dc, 0, 0, width, height, device_context, 0, 0, width, height, win32con.SRCCOPY)
        
        ctypes.windll.gdi32.GetDIBits(compatible_dc, bitmap.handle, 0, bmp.bmHeight, buf, ctypes.byref(bi), win32con.DIB_RGB_COLORS)

        img = Image.frombuffer('RGB', (bmp.bmWidth, bmp.bmHeight), buf, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(bitmap)
        win32gui.DeleteObject(device_context)
        win32gui.ReleaseDC(self.hWnd, device_context)

        # screenshot = ImageGrab.grab(position)

        screenshot = np.array(img)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        cv2.imshow("Screen", screenshot)


