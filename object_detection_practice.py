# -*- coding: utf-8 -*-
"""Object Detection Practice

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JZJyT11JJonkXfnaU5ztCEVbfHcm22Fw

# Understanding the Basics of Object Detection

https://lilianweng.github.io/lil-log/2017/10/29/object-recognition-for-dummies-part-1.html#image-gradient-vector
"""

import numpy as np
import scipy, imageio
import scipy.signal as sig
import matplotlib.pyplot as plt
import skimage.segmentation
# With mode="L", we force the image to be parsed in the grayscale, so it is
# actually unnecessary to convert the photo color beforehand.
img = imageio.imread("manu-2004.jpg", pilmode="L")

kernelX = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
kernelY = np.array([[1,1,1], [0,0,0], [-1,-1,-1]])

G_x = sig.convolve2d(img, kernelX, mode='same') 
G_y = sig.convolve2d(img, kernelY, mode='same')

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.imshow(G_x, cmap='gray'); ax1.set_xlabel('Gx')
ax2.imshow(G_y, cmap='gray'); ax2.set_xlabel('Gy')

#Load pictures
#img2 = imageio.imread("Test_Image_2.jpeg")
#img3 = imageio.imread("Test_Image_3.jpg")
#img4 = imageio.imread("Test_Image_4.jpg")
#img5 = imageio.imread("Test_Image_5.jpg", as_gray=True)

def segment(image, k_grain):
  mask_1 = skimage.segmentation.felzenszwalb(image, scale=k_grain)
  print("Mask_1 complete")
  mask_2 = skimage.segmentation.felzenszwalb(image, scale=k_grain*10)
  print("Mask_2 complete")

  fig = plt.figure(figsize=(12,5))
  ax1 = fig.add_subplot(121)
  ax2 = fig.add_subplot(122)
  a_label = "k=" + str(k_grain)
  b_label = "k=" + str(k_grain*10)

  ax1.imshow(mask_1, cmap='gray'); ax1.set_xlabel(a_label)
  ax2.imshow(mask_2, cmap='gray'); ax2.set_xlabel(b_label)

  fig.suptitle("Example Image Segmentation")
  plt.tight_layout()
  plt.show()

mask_1 = skimage.segmentation.felzenszwalb(img2, scale=75)

segment(img3, 100)

segment(img5, 100)

