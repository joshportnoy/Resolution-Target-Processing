# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:21:22 2018

@author: Josh
"""

from PIL import Image
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

import Picture as P

analyze = 'y'
while analyze == 'y':
	close('all')
	plt.ion() #switches to interactive mode to allow commands while displaying
	pict = P.Picture()
	gotContrast = False	
	ratios = []
	
	dynRangeCheck = input('\nAdjust dynamic range? (y/n) ')
	if dynRangeCheck == 'y':
		pict.bitdepthCam = int(input('What is the camera bitdepth? '))  #8			#12 for images past 4/21/18
		pict.bitdepthIm = int(input('What is the image bitdepth? ')) #16	#16 for images past 4/21/18
		pict.adjustDynamicRange()
		print('Dynamic range adjusted')
	else:
		print('Dynamic range NOT adjusted')	
		
	doTask = 'y'
	while doTask == 'y':
	
		print('\nWhich task?')
		option = input("display = d \nget contrast = a \nadd contours = c \nanalyze strip = s \nshift image = b ")
		if option == 'd':
			pict.plotImage(pict.im, 'Main Image',(0,0,1,1), False)
			cropCheck = input('Crop image? (y/n) ')
			if cropCheck == 'y':
				while cropCheck == 'y':
					pict.cropImage()
					cropCheck = input('Redo crop area? (y/n) ')
				if (input('Save crop? (y/n) ') == 'y'):
					pict.im = pict.imCrop
					pict.px = None
					pict.px = pict.imCrop.load() 
			
		elif option=='a':
			ratio = pict.getContrast()
			contrastCheck = input('Adjust to this contrast? (y/n) ')
			if contrastCheck == 'y':
				pict.adjustContrast(ratio)
				gotContrast = True		
			elif contrastCheck == 'n':
				print('Contrast NOT changed')

		elif option == 'b':
			boxShift = pict.inputBox()
			self.imShift = self.im.crop(boxShift)
			pict.plotImage(pict.imShift, 'Shifted Image', (0,0,1,1), False)

		elif option == 's':
			if not gotContrast:
				print('Warning: Values NOT adjusted for full contrast')	
				
			newStripCheck = 'y'				
			while newStripCheck == 'y':
				pict.plotImage(pict.im, '', (0,0,1,1), False)
				print('Select strip')
				stripCheck = 'y'
				while stripCheck =='y':
					pict.getStrip()
					stripCheck = input('Redo strip area? (y/n) ')
				stripDir = input('Is strip Vertical - v or Horizontal - h? ')
				while (stripDir != 'v') and (stripDir != 'h'):
					print('\nInvalid direction')
					stripDir = input('Is strip Vertical - v or Horizontal - h? ')
				if stripDir == 'v':
					pict.boxStrip[2]=pict.boxStrip[0]+1
				elif stripDir == 'h':
					pict.boxStrip[3]=pict.boxStrip[1]+1
						
				doTaskStrip = 'y'
				while doTaskStrip == 'y':
					print('\nWhich task for this strip?')
					optionStrip = input("get ratio - r \nplot values - p ")
					if optionStrip == 'r':
						if stripDir == 'v':
							print('\nRatio only possible for horizontal strips')
						elif stripDir == 'h':	
							currentRatio = pict.newgetPSF()
							ratios.append(currentRatio)
					elif optionStrip == 'p':
						if stripDir == 'v':
							pict.plotStripValuesV()
						elif stripDir == 'h':
							pict.plotStripValuesH()
					else:
						print('\nInvalid task')
					doTaskStrip = input('\nAnother task for this strip? (y/n) ')
				print('Ratios for strips entered: '+str(ratios))	
				newStripCheck = input('New strip? (y/n) ')	
				
		elif option == 'c':
			numImages = int(input('How many images to add? '))
			print('\nWhich task?')
			adjustment = input('Align vertically - shift \nNo shift - none \n')
			images = pict.multipleImages(numImages,adjustment)
			pict.makeContours(images)
		elif option == 'e':
			pict.getStrip()
			pict.boxStrip[2]=pict.boxStrip[0]+1
			pict.plotStripValuesV()	
			
		elif option == 'x':
			centroid = pict.getCOM()	
			print('Center: ' +str(centroid))
		else:
			print('\nInvalid task')
		doTask = input('Another task? (y/n) ')
		shift = None

	analyze = input('Another image? (y/n) ')