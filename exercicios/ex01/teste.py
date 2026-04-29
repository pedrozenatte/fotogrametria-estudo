import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('simple.jpg', cv.IMREAD_GRAYSCALE)

# Criar ORB
orb = cv.ORB_create()

# Detectar keypoints
kp = orb.detect(img, None)

# Calcular descritores
kp, des = orb.compute(img, kp)

# Desenhar
img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)

plt.imshow(img2)
plt.show()