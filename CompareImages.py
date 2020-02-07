import cv2
import numpy as np
im1 = cv2.imread('87.tif') #Image to be registered
im2 = cv2.imread('Mouse_p56_1.tif') #Reference image

img1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

resizedImg = cv2.resize(img2,None,fx=0.1,fy=0.1,interpolation=cv2.INTER_CUBIC)
#cv2.imshow("Image 1: ", resizedImg)
#cv2.waitKey(0)

#Initiate ORB
orb = cv2.ORB_create(50)

#Create keypoints and descriptors for both images
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)

#Match descriptors
matches = matcher.match(des1, des2, None)
matches = sorted(matches, key=lambda x: x.distance)

points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = kp1[match.queryIdx].pt
    #print(points1[i, :])
    points2[i, :] = kp1[match.trainIdx].pt
    #print(points1[i, :])

#Create homography matrix h
h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
print(h)

#Use homography
height, width = resizedImg.shape
print("size image 2: ", resizedImg.shape)
print("size image 1: ", img1.shape)

im1Reg = cv2.warpPerspective(im1, h, (width, height))
img3 = cv2.drawMatches(im1, kp1, im2, kp2, matches[:10], None)

cv2.imshow("Keypoint matches: ", img3)
#cv2.imshow("Registered image", im1Reg)
cv2.waitKey(0)


