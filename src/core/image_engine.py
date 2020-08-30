from .bitmap_header import BITMAPINFOHEADER
import win32gui
import win32con
import win32api
import ctypes

from PIL import Image


def get_hwnd_screen_buffer(hwnd, scale):

    rect = win32gui.GetWindowRect(hwnd)

    width = int((rect[2] - rect[0]) * scale)
    height = int((rect[3] - rect[1]) * scale)

    device_context = win32gui.GetWindowDC(hwnd)
    compatible_dc = win32gui.CreateCompatibleDC(device_context)
    
    win32gui.SetStretchBltMode(compatible_dc, win32con.COLORONCOLOR)

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

    win32gui.DeleteObject(bitmap)
    win32gui.DeleteObject(device_context)
    win32gui.DeleteDC(compatible_dc)
    win32gui.ReleaseDC(hwnd, device_context)

    return Image.frombuffer('RGB', (bmp.bmWidth, bmp.bmHeight), buf, 'raw', 'BGRX', 0, 1)
