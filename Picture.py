# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:19:00 2018

@author: Josh
"""

from PIL import Image
from PIL import ImageChops
from pylab import *
import io
import pathlib
import math

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mping
import matplotlib.colors as clrs
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import ndimage

import Picture as P

class Picture:
	def __init__(self):
		self.pathImage = input("File path? ")
		self.im = Image.open(self.pathImage).convert('F')
		self.imCrop = self.im
		self.imShift = self.im

		self.px = None 
		self.pxShift = None			

		self.figNum = 1
		self.cmap = 'magma' 
		self.bitdepthCam = 1
		self.bitdepthIm = 1
		self.boxCrop = [0,0,self.im.size[0],self.im.size[1]]
		self.boxStrip = (0,0,1,1)
		self.boxWhite = (0,0,1,1)
		self.boxBlack = (0,0,1,1)	

	def inputBox(self):
		box = []
		left = input("Left: ")
		box.append(int(left))
		upper = input("Upper: ")
		box.append(int(upper))	
		right = input("Right: ")
		box.append(int(right))
		lower = input("Lower: ")
		box.append(int(lower))
		return (box)
	
	def cropImage(self):
		boxCrop = self.inputBox()
		self.imCrop = self.im.crop(boxCrop)
		self.plotImage(self.imCrop, 'Cropped Image', (0,0,100,100), False)
		self.boxCrop = boxCrop
		
	def getStrip(self):
		self.plotImage(self.im, '', (0,0,100,100), False)
		
		boxStrip = self.inputBox()
		
		self.plotImage(self.im, 'Selected Strip', boxStrip, True)
		self.boxStrip = boxStrip

	def stripValuesH(self, box):
		self.imCrop = self.im.crop(box)
		pixels = list(self.imCrop.getdata())
		
		minimum = min(pixels)
		maximum = max(pixels)
		i=0
		while i < len(pixels):
			if pixels[i] == maximum:
				locationMax = i+box[0]
			if pixels[i] == minimum:
				locationMin = i+box[0]	
			i+=1
		print('Max: '+str(maximum)+', Location Max: '+str(locationMax))
		print('Min: '+str(minimum)+', Location Min: '+str(locationMin))
		return (pixels, (maximum, minimum, locationMax, locationMin))		

	def stripValuesV(self, box):
		self.imCrop = self.im.crop(box)
		pixels = list(self.imCrop.getdata())
		
		minimum = min(pixels)
		maximum = max(pixels)
		i=0
		while i < len(pixels):
			if pixels[i] == maximum:
				locationMax = i+box[1]
			if pixels[i] == minimum:
				locationMin = i+box[1]	
			i+=1
		print('Max: '+str(maximum)+', Location Max: '+str(locationMax))
		print('Min: '+str(minimum)+', Location Min: '+str(locationMin))
		return (pixels, (maximum, minimum, locationMax, locationMin))		

	def plotStripValuesH(self):
		pxValuesStrip, extrema = self.stripValuesH(self.boxStrip)	
		
		stripX = self.boxStrip[0] 	#initial X
		stripY = self.boxStrip[1]	#initial Y
		stripWidth = self.boxStrip[2] - self.boxStrip[0]
		pxX = np.linspace(stripX,(stripX+stripWidth-1), (stripWidth))
		pxY = np.array(pxValuesStrip)
		
		fig, axs = plt.subplots(figsize=(7, 7))
		plt.plot(pxX, pxY, 'bo', label='Pixel Values')

		'Fit of pixel values'
		#N = 1000
		#pxValuesFit = np.polyfit(pxX, pxY, 2)
		#p = np.poly1d(pxValuesFit)
		#pxXNew = np.linspace(pxX[0],pxX[-1], N)
		#pxYNew = p(pxXNew)
		#plt.plot(pxXNew, pxYNew, 'r.:', label='Fit')
		#plt.axis([stripX, stripWidth+stripX, minimum-5, maximum+5])
		#fig.suptitle('Pixel Values', fontsize=16)
		#plt.legend()
		#plt.show()
		return (pxValuesStrip, pxX, pxY) 

	def plotStripValuesV(self):
		pxValuesStrip, extrema = self.stripValuesV(self.boxStrip)
		
		stripX = self.boxStrip[0] 	#initial X
		stripY = self.boxStrip[1]	#initial Y
		stripHeight = self.boxStrip[3] - self.boxStrip[1]
		pxX = np.array(pxValuesStrip)
		pxY = np.linspace(stripY,(stripY+stripHeight-1), (stripHeight))	

		fig, axs = plt.subplots(figsize=(7, 7))
		plt.plot(pxX, pxY, 'bo', label='Pixel Values')

		'Fit of pixel values'
		#N = 1000
		#pxValuesFit = np.polyfit(pxX, pxY, 2)
		#p = np.poly1d(pxValuesFit)
		#pxXNew = np.linspace(pxX[0],pxX[-1], N)
		#pxYNew = p(pxXNew)
		#plt.plot(pxXNew, pxYNew, 'r.:', label='Fit')
		#plt.axis([stripX, stripWidth+stripX, minimum-5, maximum+5])
		#fig.suptitle('Pixel Values', fontsize=16)
		#plt.legend()
		#plt.show()
		
		return (pxValuesStrip, pxX, pxY) 	

	def newgetPSF(self):
		k=0
		ratioValues = []
		n = int(input("\nNumber of Strips? "))
		box = self.boxStrip
		while k<n:
			pxValuesStrip, extrema = self.stripValuesH(box)
			minimum = extrema[1]
			maximum = extrema[0]
			ratio = float(minimum/maximum)
			ratioValues.append(ratio)
			box[1] = box[1]+1
			box[3] = box[1]+1
			k+=1
		finalRatio= sum(ratioValues)/float(len(ratioValues))
		print("Ratio Values for " +str(n)+ " strips: ", ratioValues)
		print("Final Ratio:", float(finalRatio))
		width = float(input("Width of group and element? "))
		pointSpreadFunction = float(width/1.96)
		print("Point Spread Function:", pointSpreadFunction)
		return finalRatio

	def getContrast(self):
		whiteCheck = 'y'
		blackCheck = 'y'
		
		self.plotImage(self.im, '', self.boxWhite, False)
		while whiteCheck == 'y':
			print('\nChoose white area:')
			self.boxWhite = self.inputBox()
			self.plotImage(self.im, 'White Area', self.boxWhite, True)
			whiteCheck = input('Redo white area? (y/n) ')		
		
		while blackCheck == 'y':
			print('\nChoose black area:')
			self.boxBlack = self.inputBox()
			self.plotImage(self.im, 'Black Area', self.boxBlack, True)
			blackCheck = input('Redo black area? (y/n) ')
					
		pxValuesWhite, no = self.stripValuesH(self.boxWhite)
		whiteAvg = np.mean(pxValuesWhite)
		pxValuesBlack, nope = self.stripValuesH(self.boxBlack)
		blackAvg = np.mean(pxValuesBlack)

		colorRatio = (2**(self.bitdepthCam-1))/whiteAvg
		print('Black value: ' +str(blackAvg)+ ', White value: ' +str(whiteAvg)+ ', Ratio: ' +str(colorRatio))
		return (colorRatio)
	def adjustContrast(self, colorRatio):
		self.im = self.im.point(lambda i: i*colorRatio)
		self.px = self.im.load()
	def adjustDynamicRange(self):
	
		ratioDynRange = float(((2**self.bitdepthCam)/(2**self.bitdepthIm)))
		print('Ratio: '+ str(ratioDynRange))
		self.im = self.im.point(lambda i: i*ratioDynRange)
		
		pxDyn = np.array(self.im.getdata())
		pxDyn = floor(pxDyn)
		self.im.putdata(pxDyn)
		self.px = self.im.load() 

	def plotImage(self, image, title, boxStrip, draw):
		fig = plt.figure()
		ax = plt.gca()
		figure = plt.imshow(np.array(image), cmap=self.cmap)
	
		divider = make_axes_locatable(ax)
		cax = divider.append_axes("right", size="5%", pad=0.04)
		plt.colorbar(figure, cax=cax) 
		fig.suptitle(str(title), fontsize=16)
		if draw == True:
			rect = plt.Rectangle(
			(boxStrip[0], boxStrip[3]), 
			(boxStrip[2]-boxStrip[0]) , (boxStrip[1]-boxStrip[3]), 
			fill=False, edgecolor = "white")
			ax.add_patch(rect)	
		plt.show()	
		self.figNum+=1
		return			

	def getContour(self, colorFig):
		(min, max) = self.im.getextrema()
		conLevel = ((max-min)/2) + min
#		contourLevel.append(conLevel)
		print('Contour Level: ' +str(conLevel))
		figContour = plt.contour(self.im, levels = [conLevel], linewidths = .7, 
								colors = (colorFig, '#afeeee', '0.5'))
		#clabel(figContour, fontsize = 'xx-small') 
		return figContour		
	def makeContours(self,images):
		figCont = plt.figure()
		axCont = plt.gca()		
		morecont = 1
		contourLevel = []

		num_colors = len(images)+1
		cm = mpl.cm.get_cmap(name='gist_gray')
		colors = [cm(1.*i/num_colors) for i in range(num_colors)]

		currentColor = colors[0]	
		figContour = self.getContour(colors[0])

		i=0
		while i<len(images): 
			currentColor = colors[i+1]
			currentIm = images[i]
			figContour = currentIm.getContour(currentColor)
			i+=1
			
		figMain = plt.imshow(np.array(self.im), cmap = self.cmap, vmin=0)
		divider = make_axes_locatable(axCont)
		cax = divider.append_axes("right", size="5%", pad=0.04)
		figCont.colorbar(figMain, cax=cax)
		figCont.suptitle('Contour Plot', fontsize=16)

		plt.show()	
	
	def multipleImages(self, numImages, adjustment):
		images = []
		i=0
		if adjustment == 'none':
			while i <numImages:
				print("\nImage: "+str(i+2))
				pictNew = P.Picture()
				pictNew.im = pictNew.im.crop(self.boxCrop)
				pictNew.px = pictNew.im.load()
				images.append(pictNew)
				i+=1

		elif adjustment == 'shift':
			stripBox = [0,0,1,1]
			print('\nSelect vertical strip for centering')
			stripCheck = 'y'
			while stripCheck == 'y':
				stripBox = self.inputBox()
				stripBox[2] = stripBox[0]+1
				self.plotImage(self.im, '', stripBox, True)
				stripCheck = input('Redo strip area? (y/n) ')
			print('stripBox: '+str(stripBox))
			px,locationMax = self.stripValuesV(stripBox,1)

			imageTitles = list(range(2,numImages+2))
			while i < numImages:
				imageTitle = 'image'+str(imageTitles[i])
				print("\nImage: "+str(i+2))
				imageTitle = P.Picture()
				imageTitle.im = imageTitle.im.crop(self.boxCrop)
				imageTitle.px = imageTitle.im.load()
				imageTitle.shiftingImage(locationMax)
				images.append(imageTitle)
				i+=1
		else:
			print('incorrect option')	
		return images
			
	def shiftingImage(self, locationMax):
		self.plotImage(self.im, '', (0,0,1,1), False)
		centeringCheck = 'y'
		while centeringCheck == 'y':
			print('Select vertical strip for centering')
			stripBoxNew = self.inputBox()
			stripBoxNew[2] = stripBoxNew[0]+1
			self.plotImage(self.im, '', stripBoxNew, True)
			centeringCheck = input('Redo strip area? (y/n) ')
			
		stripBoxNew[2] = stripBoxNew[0]+1
		pxNew,locationMaxNew = self.stripValuesV(stripBoxNew,1)
		
		
		diff = locationMax - locationMaxNew
		print('diff: '+str(diff))
		
		boxShiftNew = [0, 0-diff, self.im.size[0], self.im.size[1]-diff]				
		self.imShift = self.im.crop(boxShiftNew)
		
		backgndCheck = 'y'
		while backgndCheck == 'y':
			print('Select background')
			stripBackgnd = self.inputBox()
			self.plotImage(self.im, '', stripBackgnd, True)
			backgndCheck = input('Redo strip area? (y/n) ')
		pxValuesBackgnd, nothing = self.stripValues(self.boxWhite,(self.boxWhite[2] -self.boxWhite[0]))
		pxBackgnd = np.mean(pxValuesBackgnd)	
		print('background value: ' +str(pxBackgnd))
		
		stripBoxFill=(0,0,self.im.size[0],diff)
		self.imShift.paste(pxBackgnd, box=(0,0,self.im.size[0],diff))
		self.plotImage(self.imShift, 'supposably shifted image', stripBoxFill, True)
		
		self.im = self.imShift
		self.px = self.im.load()
		
		self.plotImage(self.im, 'pictNew', (0,0,1,1), False)

	def shiftPx(self, boxShift):
		x = 0
		y = 0
		self.px = self.im.load()
		
		
		xInit = boxShift[0]
		yInit = boxShift[1]
		
		
		while y <= (boxShift[3]-boxShift[1]):
			while x <= (boxShift[2]-boxShift[0]):
				self.pxShift[x,y] = self.px[(xInit+x),(yInit+y)]
				x += 1
			y += 1
		self.pxShift = self.pxShift.load()
		print(str(self.pxShift[1,1]))
		
	def getCOM(self):
		#imgname = "/Users/daniel/Desktop/rad2.tiff"
		#imgmatrix = imread(imgname, flatten=True)
		pixels = np.array(self.im.getdata())
		print('pixels: ' +str(pixels))
		
		centroid = ndimage.measurements.center_of_mass(pixels)
		return centroid