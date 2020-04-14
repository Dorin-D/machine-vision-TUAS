Requirements:
Python 3.7
pip package installer

To install necessary libraries, open a command line interpreter, browse to installation folder and run:
pip3 install -r requirements.txt
OR,
pip install -r requirements.txt

To execute this program, run:
python3 main.py
OR
python main.py

Program instructions:
1) Select input .tif image
2) Select output folder
3) If using a black background image, tick "Black background"
4) Type kernel size, value has to be non negative odd numbers
5) Insert threshold
6) Choose option
	* "Contour only" outputs the contours of detected slices
	* "Content only" outputs the brains of detected slices
	* "Contour and content" outputs the contours in the output folder and the brains in a separate "contents" folder.
7) Press "Process Image".

Result: Output images should be directed in the chosen output folder.