import cv2, sys
import os.path

def blur_picture(filename, blackBG, k):
	# read and display the original image
	image = cv2.imread(filename = filename)
	if not(blackBG):
		image = cv2.bitwise_not(image)
	# blur and grayscale before thresholding
	blur = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(
		src = blur, 
		ksize = (k, k), 
		sigmaX = 0)

	# perform adaptive thresholding 
	(t, maskLayer) = cv2.threshold(src = blur, 
		thresh = 0, 
		maxval = 255, 
		type = cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	# make a mask suitable for color images
	mask = cv2.merge(mv = [maskLayer, maskLayer, maskLayer])
	# use the mask to select the "interesting" part of the image
	sel = cv2.bitwise_and(src1 = image, src2 = mask)

	# output the result
	outputFile = "imagewithblur.png"
	cv2.imwrite(outputFile, img = sel)
	return outputFile

		
if __name__ == "__main__":
	filename = sys.argv[1]
	k = int(sys.argv[2])
	blur_picture(filename, False, k)
