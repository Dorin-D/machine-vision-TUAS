'''
 * Python program to use contours to count the objects in an image.
 *
 * usage: python Contours.py <filename> <threshold>
'''

import os
import numpy as np
import cv2, sys
"""
	functions to allow sorting the slices, in case there is a need to have the images ordered
"""
def get_min_by_col(li, col, j):
	"""
	li is the list of contours
	j is the shape index of the list of contours
	col is the column by which you want to sort (x or y position)
	"""
	minValue = li[j][0][0][col]
	"""
		first 0 is the pixel is the first pixel in the list of contours
		second 0 is a "buffer" index as the pixels are stored as a list element within a list (e.g. [[25, 12]])
	"""
	for i in range(0, len(li[j])):
		if li[j][i][0][col] < minValue:
			minValue = li[j][i][0][col]
	return minValue

def quicksort(myList, start, end, contourList):
	if start < end:
		pivot = partition(myList, start, end, contourList)
		quicksort(myList, start, pivot-1, contourList)
		quicksort(myList, pivot+1, end, contourList)

def partition(myList, start, end, contourList):
	pivot = myList[start]
	left = start+1
	right = end
	done = False
	while not done:
		while left <= right and myList[left] <= pivot:
			left = left + 1
		while myList[right] >= pivot and right >= left:
			right = right - 1
		if right < left:
			done = True
		else:
			myList[left],myList[right] = myList[right],myList[left]
			contourList[left],contourList[right] = contourList[right],contourList[left]
	myList[start],myList[right] = myList[right],myList[start]
	contourList[start],contourList[right] = contourList[right],contourList[start]
	return right



def contour_picture(filename, outline, blackBG, t, outputName):
	image = cv2.imread(filename = filename)

	# create binary image
	gray = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(src = gray, 
		ksize = (5, 5), 
		sigmaX = 0)
	(t, binary) = cv2.threshold(src = blur,
		thresh = t, 
		maxval = 255, 
		type = cv2.THRESH_BINARY)

	if not(blackBG):
		image = cv2.bitwise_not(image)
		
	# find contours
	(contours, _) = cv2.findContours(image = binary, 
		mode = cv2.RETR_EXTERNAL,
		method = cv2.CHAIN_APPROX_SIMPLE)

	contours_size_filter = []
	#filter contour to shapes bigger than 200 to avoid garbage data from being shown
	for (i, c) in enumerate(contours):
		if len(c) > 200:
			contours_size_filter.append(contours[i])
	print("Trimmed down to %d objects." % len(contours_size_filter))

	#sorting the shapes by the leftermost pixel, can be removed and the base functionality works
	minXPixels = []
	for (i,c) in enumerate(contours_size_filter):
		minXPixels.append(int(get_min_by_col(contours_size_filter, 0, i)))
	quicksort(minXPixels, 0, len(minXPixels)-1, contours_size_filter)
	
	# draw contours over original image according to outline parameter
	#0 = outline only, 1 = content only, 2 = content and outline, outlines being in a separate folder
	if outline == 0:
		image[np.where((image>[0,0,0]).all(axis=2))] = [0,0,0]
		cv2.drawContours(image = image, 
		contours = contours_size_filter, 
		contourIdx = -1, 
		color = (0, 0, 255), 
		thickness = 5)
	elif outline == 1:
		pass
	elif outline == 2:
		#creating folders for the separate outline output
		if not os.path.exists(outputName):
			os.makedirs(outputName)
		if not os.path.exists(outputName+"/outlines"):
			os.makedirs(outputName+"/outlines")
		for (i, c) in enumerate(contours_size_filter):
			(x, y, w, h) = cv2.boundingRect(c)
			crop_img = image[y:y+h, x:x+w]
			cv2.imwrite(outputName+"/outlines/"+str(i)+".tif", img = crop_img)

		image[np.where((image>[0,0,0]).all(axis=2))] = [0,0,0]
		cv2.drawContours(image = image, 
		contours = contours_size_filter, 
		contourIdx = -1, 
		color = (0, 0, 255), 
		thickness = 5)
		
	if not os.path.exists(outputName):
		os.makedirs(outputName)
	for (i, c) in enumerate(contours_size_filter):
		(x, y, w, h) = cv2.boundingRect(c)
		crop_img = image[y:y+h, x:x+w]
		cv2.imwrite(outputName+"/"+str(i)+".tif", img = crop_img)
		
	#line to save the full image with contours
	#cv2.imwrite("imagewithcontours.tif", img = image)

if __name__ == "__main__":
	filename = sys.argv[1]
	t = int(sys.argv[2])
	contour_picture(filename, 2, False, t, "./output")