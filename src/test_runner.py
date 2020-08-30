import cv2
import time
import keyboard
import numpy as np

from core.maplecore import MapleCore


# core = MapleCore('StoryMS', 1.0)

# core.add_buff_key('./src/resources/skill/magic_boost.png', 't')
# core.activate_window()

# core.debug_mode = True

# src, gray = core.get_game_screen()

# cv2.imshow("Screen", src)

# cv2.imwrite('./training_dataset/training/8.png', src)

# cv2.waitKey(0)


src = cv2.imread('./training_dataset/training/1.png')
gray = cv2.imread('./training_dataset/training/1.png', 0)

template = cv2.imread('./training_dataset/mob.png', 0)
reversed_template = cv2.flip(template, 1) # 좌우 반전

w, h = template.shape[::-1]
res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED) + cv2.matchTemplate(gray, reversed_template, cv2.TM_CCOEFF_NORMED)

threshold = 0.7
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(src, pt, (pt[0] + w, pt[1] + h), (0, 0,255), 2)

cv2.imshow("Detection", src)

cv2.imwrite("result.png", src)

cv2.waitKey(0)



