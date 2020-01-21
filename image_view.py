from skimage import data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

image = mpimg.imread("1.tif")
plt.imshow(image)
plt.show()