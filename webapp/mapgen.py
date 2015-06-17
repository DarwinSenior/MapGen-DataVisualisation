import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import os
import cairosvg
import json
import sys
import matplotlib.cm as cm
import database
from csv import DictReader

def limit(x, domain):
	minx, maxx = domain
	return max(minx, min(maxx-1, x))


def tmp_write(msg):
	sys.stdout.write("\033[K")
	sys.stdout.write(msg)
	sys.stdout.flush()
	sys.stdout.write("\r")

# scale x from min max to 0 and 1
def minmax_scale(x):
	x_max = np.max(x)
	x_min = np.min(x)
	return (x-x_min)/(x_max-x_min)

def linear_scale(x, domain):
	d_min, d_max = domain
	return (x-d_min)/(d_max-d_min)

def utfgrid_encode(x):
	x += 32
	if x>=34: x += 1
	if x>=92: x += 1
	return chr(x)

def utfgrid_decode(x):
	x = ord(x)
	if x>=34: x -= 1
	if x>=92: x -= 1
	return x

# we assume the x,y coord is in the range between 0 and 1
def splitData(data, info, zoom, width=256):
	size = 2**zoom
	data_group = [[[] for i in range(size+1)] for j in range(size+1)] # empty bins
	info_group = [[[] for i in range(size+1)] for j in range(size+1)]
	# put each datium to corresponding bin
	for i, datium in enumerate(data):
		left = datium[0]-datium[2] # x-a
		right = datium[0]+datium[2] # x+a
		top = datium[1]-datium[2] # y-a
		bottom = datium[1]+datium[2] # y+a

		x1 = int(left*size)
		x2 = int(right*size)
		y1 = int(top*size)
		y2 = int(bottom*size)

		if (datium[2]*size*width>1): #drawable as an pixel perspective
			data_group[x1][y1].append(datium)
			info_group[x1][y1].append(info[i])
			if y1!=y2:
				data_group[x1][y2].append(datium)
				info_group[x1][y2].append(info[i])
			if x1!=x2:
				data_group[x2][y1].append(datium)
				info_group[x2][y1].append(info[i])
			if (x1!=x2 and y1!=y2):
				data_group[x2][y2].append(datium)
				info_group[x2][y2].append(info[i])
	return data_group, info_group

def parseData(csvfile):
	raw_data = pd.read_csv(csvfile)

	data = np.zeros((len(raw_data), 6))
	data[:,0] = minmax_scale(raw_data.DEC.values) # x
	data[:,1] = minmax_scale(raw_data.RA.values) # y
	data[:,2] = raw_data.A_IMAGE.values*0.263/3600*2 # a
	data[:,3] = raw_data.B_IMAGE.values*0.263/3600*2 # b
	data[:,4] = raw_data.THETA_IMAGE.values+90.
	# data[:,5] = minmax_scale(raw_data.COLOR.values) # colour 

	# currently everything is saved as string
	csvfile.seek(0)
	header = csvfile.readline().strip().split(',')
	info = [row for row in DictReader(csvfile, header)]
	return data, info, header

# to draw the image from data and scale it with x,y
def drawSvg(data, x, y, zoom, height=256, width=256):
	size = 1/(2**zoom)
	rangex = np.array([x*size, (x+1)*size])
	rangey = np.array([y*size, (y+1)*size])

	data = data.copy()

	if data.size:
		data[:,0] = linear_scale(data[:,0], rangex)*width # x
		data[:,1] = linear_scale(data[:,1], rangey)*height # y
		data[:,2] = data[:,2]*width/size # a
		data[:,3] = data[:,3]*height/size # b
		# data[:, 4] = data[:, 4]*180/np.pi # theta

		ellipses = ''.join(map(ellipse, data))
	else:
		ellipses = ""

	return """
	<svg height="%d" width="%d">
	<rect height="100%%" width="100%%" fill="black" />
	%s</svg>
	 """%(height, width, ellipses)

def drawUTFMap(data, info, raw_img, x, y, zoom, height=256, width=256):
	size = 1/(2**zoom)
	rangex = np.array([x*size, (x+1)*size])
	rangey = np.array([y*size, (y+1)*size])

	data = data.copy()

	if data.size:
		data[:,0] = linear_scale(data[:, 0], rangex)*width/2 # x
		data[:,1] = linear_scale(data[:, 1], rangey)*height/2 # y
		data[:,2] = linear_scale(data[:, 2], [0, size])*width/2 # a
		data[:,3] = linear_scale(data[:, 3], [0, size])*height/2 # b

	# img = Image.open('%s/%d/%d/%d.png'%(path, zoom, x, y)).resize((int(width/2), int(height/2)), Image.NEAREST)
	img = Image.open(BytesIO(raw_img)).resize((int(width/2), int(height/2)), Image.NEAREST)

	# 3 is rely on the fact that it is rgb not rgba
	pixels = np.array(img.getdata()).reshape((width/2, height/2, 3))
	grid = np.zeros((width/2, height/2), dtype=np.uint8)
	new_info = {0 : {}}

	for i,datium in enumerate(data):
		x2, y2, a, b, theta, colour = datium
		center_colour = pixels[limit(y2, (0, height/2))][limit(x2, (0, width/2))]
		colorExist = False
		for y1 in range(max(int(y2-a), 0), min(int(y2+a), int(height/2))):
			for x1 in range(max(int(x2-a), 0), min(int(x2+a), int(width/2))):
				if (pixels[y1][x1]==center_colour).all():
					grid[y1][x1] = i+1
					colorExist = True
		if colorExist:
			new_info[i+1] = info[i]

	grid = ["".join(map(utfgrid_encode, line)) for line in grid]
	
	return {"grid": grid, "keys": list(new_info.keys()), "data": new_info}

# the input params shall be in the form (x, y, a, b, theta, color)
# where theta is degree and x,y,a,b is float and color in [0, 1]
def ellipse(data):
	x,y,a,b,theta,color = data
	R,G,B, _ = cm.hot(color)
	params = (x, y, a, b, theta, x, y, int(R*225), int(G*225), int(B*225))
	return '<ellipse cx="%f" cy="%f" rx="%f" ry="%f" transform="rotate(%f %f %f)" fill="#%02x%02x%02x"/>'%params

def paste(grid, gridx, offsetx, offsety):
	for x in range(0, width, 2):
		for y in range(0, height, 2):
			grid[y/2+offsety][x/2+offsetx] = utfgrid_decode(gridx[y][x])

def parseColor(data, info, expression=""):
	if data.size:
		for i, val in enumerate(info):
			color = val.get(expression) or 0
			data[i][5] = abs(float(color) - int(float(color)))

def generateByCreate(data, info, x, y, zoom, expression="", height=256, width=256):
	parseColor(data, info, expression)
	png = cairosvg.svg2png(drawSvg(data, x, y, zoom, height, width))
	jsn = json.dumps(drawUTFMap(data, info, png, x, y, zoom, height, width))
	return png,jsn


