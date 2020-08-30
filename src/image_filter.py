import os
import cv2
import numpy as np

path = './training_dataset/mask/'

masks = list(sorted(os.listdir(os.path.join("./", path))))

for img in masks[1:2]:
    file_name = path + img
    src = cv2.imread(file_name)

    # define range of blue color in HSV
    lower = np.array([122, 122, 122])
    upper = np.array([124, 124, 124])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(src, lower, upper)

    cv2.imwrite(file_name, mask)

print(masks)

cv2.waitKey(0)