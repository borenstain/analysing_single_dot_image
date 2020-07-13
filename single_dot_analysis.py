# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:30:51 2020
@author: borensta
Includes microscope image and confocal data
"""
import os
import csv
import numpy as np
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
from skimage import filters
from skimage import measure
import scipy.ndimage as ndimage 

# =============================================================================
# Loading microscope image
# Note 1.55 pixel = 1um
# =============================================================================
mono_blue=np.zeros((1024,1024))
take="200324_172832-1"
Image_file_name=take+".jpeg"
directory=os.path.dirname(r'C:\Users\borensta\Documents\work-horse\Small dots issues\confocal data\..')
Image_file=os.path.abspath(os.path.join(directory,Image_file_name))
img_color = mpimg.imread(Image_file)
# =============================================================================
# loading confocal data
# =============================================================================
cf_fnam=take+'.csv'
directory=os.path.dirname(r'C:\Users\borensta\Documents\work-horse\Small dots issues\confocal data\..')
cf_fnam=os.path.abspath(os.path.join(directory,cf_fnam))
with open(cf_fnam, newline='') as csvfile:
        cf_data_s = list(csv.reader(csvfile)) 
# =============================================================================

w1=450
w2=w1+100
h1=450
h2=h1+100
for i in range(1024):
    for j in range(1024):
        if i==w1 or i==w2 or j==h1 or j==h2:
            mono_blue[j,i]=0
        else:
            mono_blue[j,i] =float(img_color[j,i,2])
plt.figure(1)
plt.imshow(mono_blue, cmap=plt.cm.gray)
plt.title("Microscope data of all dots, take "+take)
plt.show()

single_dot=mono_blue[(h1+1):h2,(w1+1):w2]
threshold_value = filters.threshold_otsu(single_dot)

# plt.figure(2)
# plt.imshow(single_dot, cmap=plt.cm.gray)
# plt.contour(single_dot, levels=[threshold_value-30, threshold_value,threshold_value+30], linewidths=1, colors='r')
# plt.show()

plt.figure(3)
plt.imshow(single_dot, cmap=plt.cm.gray)
# Find contours at a constant value of threshold_value
contours = measure.find_contours(single_dot, threshold_value+30)

# =============================================================================
# # Display the image and plot all with contours found
# =============================================================================

for n, contour in enumerate(contours):
    plt.plot(contour[:, 1], contour[:, 0], linewidth=2)
    plt.title("Microscope contour plot single dot, take "+take)
plt.show()
# =============================================================================
# # Sortung the largest contour.
# =============================================================================

plt.figure(4)
contour_largest = sorted(contours, key=lambda x: len(x))[-1]
plt.imshow(single_dot, cmap=plt.cm.gray)
plt.plot(contour_largest [:, 1], contour_largest [:, 0], linewidth=1)
plt.title("Microscope contour around single dot, take "+take)
plt.show()

# Create an empty image to store the masked array
b_and_w = np.zeros_like(single_dot, dtype=int)
# Create a contour image by using the contour coordinates rounded to their nearest integer value
b_and_w[np.round(contour_largest[:, 0]).astype(int), np.round(contour_largest[:, 1]).astype(int)] = 1
# =============================================================================
# save the contoured image
# =============================================================================
# fname=os.path.abspath(os.path.join(directory,"b_and_w.png"))
# plt.imsave(fname, b_and_w)
# =============================================================================
# # Fill in the hole created by the contour boundary
# =============================================================================
# Carefull - I had a problem when the border was open one pixel at the edge.
b_and_w_filled = ndimage.binary_fill_holes(b_and_w).astype(int)
plt.figure(5)
# b_and_w  = ~b_and_w 
plt.imshow(b_and_w_filled,cmap=plt.cm.gray)
plt.title("Microscope isolated single dot area, take "+take)
plt.show()
dot_area=np.sum(b_and_w_filled)
print("dot area=",dot_area)

# =============================================================================
# dealing with confocal data
# =============================================================================
cf_data_s =str(cf_data_s).strip('[]').split(',')
cf_data= np.zeros((1024,1024), dtype=float)
for row in range(1024):
    for col in range(1024):
        i=col*row+col
        j=len(cf_data_s[i])-1
        cf_data[col,row]=float(cf_data_s[i][2:j])
plt.figure(6)
plt.imshow(cf_data, cmap=plt.cm.gray)
plt.title("Confocal all dots raw data, take "+take)
plt.show()
print("sum cf_data=",np.sum(cf_data), "max=", np.max(cf_data),"min =", np.min(cf_data))
threshold_value = filters.threshold_otsu(cf_data)

plt.figure(7)
plt.imshow(cf_data, cmap=plt.cm.gray)
plt.contour(cf_data, levels=[threshold_value], linewidths=1, colors='w')
plt.title("Confocal-data all dots, take "+take)
plt.show()
print(threshold_value)
# cf_scaled= np.zeros((1024,1024), dtype=float)

for i in range(1024):
    for j in range(1024):
        if i==w1 or i==w2 or j==h1 or j==h2:
            cf_data[j,i]=8
        else:
            cf_data[j,i] =float(cf_data[j,i])
plt.figure(8)
plt.imshow(cf_data, cmap=plt.cm.gray)
plt.title("take "+take+", Confocal-data selected dot")
plt.show()

single_cf_dot=cf_data[(h1+1):h2,(w1+1):w2]
plt.figure(9)
plt.imshow(single_cf_dot, cmap=plt.cm.gray)
plt.plot(contour_largest [:, 1], contour_largest [:, 0], linewidth=1)
plt.title("Confocal-data zoon in the selected dot, take "+take)
plt.show()

# skimage.measure.find_contours(array, level, fully_connected='low', positive_orientation='low', *,
# https://stackoverflow.com/questions/48888239/finding-the-center-of-mass-in-an-image