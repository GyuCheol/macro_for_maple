import cv2
import time
import keyboard
import numpy as np

from core.maplecore import MapleCore


core = MapleCore('StoryMS', 1.0)

core.add_buff_key('./src/resources/skill/meditation.png', 't', 1.5)
core.activate_window()

core.add_mob('./src/resources/mob/9420510/1.png')

core.debug_mode = True


while True:
    # src, gray = core.get_game_screen()
    # print(core.get_name_location(gray))
    # time.sleep(1)
    core.progress(
        use_buff=True,
        use_mob_detect=True,
        use_medal_detect=True
        )

    cv2.imshow("Detection", core.lastest_detection_screen)
    cv2.waitKey(delay=3000)



# src, gray = core.get_game_screen()

# cv2.imshow("Screen", src)

# cv2.imwrite('./training_dataset/training/8.png', src)

# cv2.waitKey(0)


# src = cv2.imread('./training_dataset/training/1.png')
# gray = cv2.imread('./training_dataset/training/1.png', 0)

# reversed_template = cv2.flip(template, 1) # 좌우 반전

# template = cv2.imread('./training_dataset/mob.png', 0)
# w, h = template.shape[::-1]
# res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED) + cv2.matchTemplate(gray, reversed_template, cv2.TM_CCOEFF_NORMED)

# threshold = 0.7
# loc = np.where( res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(src, pt, (pt[0] + w, pt[1] + h), (0, 0,255), 2)

# cv2.imshow("Detection", src)

# cv2.imwrite("result.png", src)

# cv2.waitKey(0)



