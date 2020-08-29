import cv2

from image_engine.maplecore import MapleCore

core = MapleCore('Windia (1600x900)', 2.0)

# core.activate_window()
core.get_window_screen()
# core.set_window_size(2400, 1350)

# core.add_buff_key()

cv2.waitKey(5000)


