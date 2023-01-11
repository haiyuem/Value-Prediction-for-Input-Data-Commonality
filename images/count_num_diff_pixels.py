# This script counts the number of different pixels between two images. 
# R/G/B are counted separately so the total sum is width*height*#channels(3)


#### Results:
# ('no diff: ', 100853, 'percent: ', 8.92)
# ('diff < 5: ', 518574, 'percent: ', 45.87)
# ('diff < 10: ', 702722, 'percent: ', 62.16)

import numpy as np
import cv2

img1 = cv2.imread('self_driving_captured_frames/resized_1024X368/00000.jpg')
img2 = cv2.imread('self_driving_captured_frames/resized_1024X368/00001.jpg')

diff = cv2.absdiff(img1, img2)
sum = float(img1.size)
diff0 = np.sum(diff==0)
diff5 = np.sum(diff<5)
diff10 = np.sum(diff<10)
print("======Difference between two images: counting each R/G/B individually======")
print("no diff: ", diff0, "percent: ", round(100*(diff0/sum), 2))
print("diff < 5: ", diff5, "percent: ", round(100*(diff5/sum), 2))
print("diff < 10: ", diff10, "percent: ", round(100*(diff10/sum), 2))
