import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import blurpicture
import contour
import cv2

##TO DO

class App(QWidget):

	def __init__(self):
		self.labImage = ''
		self.outputFolder = ''
		super().__init__()
		self.title = 'Machine Vision - Brain Analysis'
		self.left = 30
		self.top = 60
		self.width = 640
		self.height = 480
		self.x = 0
		self.y = 0
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		
		#input browse button
		self.inputLabel = QLabel(self)
		self.inputLabel.setText("Select input .tif image")
		self.inputLabel.move(20, 20)
		self.inputBrowseButton = QPushButton("Browse", self)
		self.inputBrowseButton.setToolTip("Use this button to select the image")
		self.inputBrowseButton.move(20, 40)
		self.inputBrowseButton.resize(80, 30)
		self.inputBrowseButton.clicked.connect(self.pickFile)
		
		#output browse button
		self.outputLabel = QLabel(self)
		self.outputLabel.setText("Select output folder")
		self.outputLabel.move(20, 80)
		self.outputBrowseButton = QPushButton("Browse", self)
		self.outputBrowseButton.setToolTip("Use this button to select the output folder")
		self.outputBrowseButton.move(20, 100)
		self.outputBrowseButton.resize(80, 30)
		self.outputBrowseButton.clicked.connect(self.pickFolder)
		
		#black or white background
		self.blackBackground = QCheckBox("Black background", self)
		self.blackBackground.move(20, 140)
		
		#kernel size argument
		self.kernelSizeLabel = QLabel(self)
		self.kernelSizeLabel.setText("Insert kernel size:")
		self.kernelSizeLabel.move(20, 160)
		self.kernelSizeBox = QLineEdit(self)
		self.kernelSizeBox.move(20, 180)
		self.kernelSizeBox.resize(60, 20)
		#threshold argument
		self.thresholdLabel = QLabel(self)
		self.thresholdLabel.setText("Insert threshold:")
		self.thresholdLabel.move(20, 200)
		self.thresholdBox = QLineEdit(self)
		self.thresholdBox.move(20, 220)
		self.thresholdBox.resize(60, 20)
		#out settings
		self.comboBox = QComboBox(self)
		self.comboBox.addItem("Contour only")
		self.comboBox.addItem("Content only")
		self.comboBox.addItem("Contour and content")
		self.comboBox.move(20, 270)
		
		
		#process image button
		self.simpButton = QPushButton("Process image", self)
		self.simpButton.move(100, 300)
		self.simpButton.resize(100,40)
		self.simpButton.clicked.connect(self.processImage)
		
		self.show()
		

	def pickFile(self):
		title = "Select an input .tif file"
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self, title, "Browse Image", "","All Files (*);;Tif Files (*.tif)", options=options)
		if fileName:
			self.labImage = fileName
			
	def pickFolder(self):
		title = "Select an output folder"
		flags = QFileDialog.ShowDirsOnly
		dirpath = str(QFileDialog.getExistingDirectory(self, title, '', flags))
		if dirpath:
			self.outputFolder = dirpath

	def processImage(self):
		try:
			kernelSize = int(self.kernelSizeBox.text())
			threshold = int(self.thresholdBox.text())
			blackBackground = self.blackBackground.isChecked()
			text = str(self.comboBox.currentText())
			if text == "Contour only":
				outline = 0
			elif text == "Content only":
				outline = 1
			else:
				outline = 2			
			blurredPicture = blurpicture.blur_picture(self.labImage, blackBackground, kernelSize)
			contour.contour_picture(blurredPicture, outline, blackBackground, threshold, self.outputFolder)
		except cv2.error as e:
			error_dialog = QMessageBox()
			error_dialog.setText('Kernel size must be an odd number.')
			error_dialog.setIcon(QMessageBox.Critical)
			error_dialog.setWindowTitle("Kernel Size Error")
			error_dialog.exec_()


def GUI():
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())