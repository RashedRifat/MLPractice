# -*- coding: utf-8 -*-
"""Image Segmentation Practice

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hwJLocdh9CMIZHCuWHaDLBoTwHMiQjke

##Split Into Background and Foreground


from: https://www.analyticsvidhya.com/blog/2019/04/introduction-image-segmentation-techniques-python/?utm_source=blog&utm_medium=computer-vision-implementing-mask-r-cnn-image-segmentation
"""

# Commented out IPython magic to ensure Python compatibility.
from skimage.color import rgb2gray
import numpy as np
import cv2
import matplotlib.pyplot as plt
# %matplotlib inline
from scipy import ndimage
import tensorflow as tf

image = plt.imread('pic1.jpeg')
image.shape
plt.imshow(image)

gray = rgb2gray(image)
plt.imshow(gray, cmap='gray')

gray.shape

gray_r = gray.reshape(gray.shape[0]*gray.shape[1])

for i in range(gray_r.shape[0]):
  if gray_r[i] > gray_r.mean():
    gray_r[i] = 1
  else:
    gray_r[i] = 0
gray = gray_r.reshape(gray.shape[0], gray.shape[1])
plt.imshow(gray, cmap='gray')

"""##Edge Detection Segmentation"""

edge_image = plt.imread('pic2.png')
#plt.imshow(edge_image)
gray_edge = rgb2gray(edge_image)
plt.imshow(gray_edge, cmap='gray')

#Sobel Kernels
sobel_horizontal = np.array([np.array([1, 2, 1]), np.array([0, 0, 0]), np.array([-1, -2, -1])])
print(sobel_horizontal, 'is a kernel for detecting horizontal edges')
sobel_vertical = np.array([np.array([-1, 0, 1]), np.array([-2, 0, 2]), np.array([-1, 0, 1])])
print(sobel_vertical, 'is a kernel for detecting vertical edges')

#Convolve this over the mage
out_h = ndimage.convolve(gray_edge, sobel_horizontal, mode='reflect')
out_v = ndimage.convolve(gray_edge, sobel_vertical, mode='reflect')
# here mode determines how the input array is extended when the filter overlaps a border.
plt.imshow(out_h, cmap='gray')

plt.imshow(out_v, cmap='gray')

"""##The Laplacian Kernel 
This allows for the detection of both horizaontal and verital edges.

The kernel is as such: 
[[1,1,1], [1,-8,1], [1,1,1]]
"""

#Setup the kernel
kernel_laplace = np.array([np.array([1,1,1]), np.array([1,-8,1]), np.array([1,1,1])])
print(kernel_laplace)

#Convolve the Laplacian Kernel over the Edge_Image 

out_edge = ndimage.convolve(gray_edge, kernel_laplace, mode='reflect')
plt.imshow(out_edge, cmap='gray')

#Apply the filter to the orignal image:

out_edge = ndimage.convolve(gray, kernel_laplace, mode='reflect')
plt.imshow(out_edge, cmap='gray')

"""##Image Segmentation based on Clustering

Here we are using k-means. 


One of the most commonly used clustering algorithms is k-means. Here, the k represents the number of clusters (not to be confused with k-nearest neighbor). Let’s understand how k-means works:

First, randomly select k initial clusters
Randomly assign each data point to any one of the k clusters
Calculate the centers of these clusters
Calculate the distance of all the points from the center of each cluster
Depending on this distance, the points are reassigned to the nearest cluster
Calculate the center of the newly formed clusters
Finally, repeat steps (4), (5) and (6) until either the center of the clusters does not change or we reach the set number of iterations
"""

#Load image and resize image into a two dimensonal array (from its 3d array)
pic = image/255 # Dividing by 255 brings the values in the range of 0 and 1
pic_n = pic.reshape(pic.shape[0]*pic.shape[1], pic.shape[2])
pic_n.shape

#Create Cluster
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=5, random_state=0).fit(pic_n)
pic2show = kmeans.cluster_centers_[kmeans.labels_]

#Display Clustered Picture
cluster_pic = pic2show.reshape(pic.shape[0], pic.shape[1], pic.shape[2])
plt.imshow(cluster_pic)