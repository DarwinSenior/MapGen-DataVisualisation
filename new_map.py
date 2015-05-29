import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import os
import cairosvg
import json
import sys
import matplotlib.cm as cm

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

# generate the higher level image
# from path/{zoom}/{x}/{y}.png from tiles (2x, 2y) (2x+1, 2y) (2x, 2y+1) (2x+1, 2y+1) of zoom+1 level
# def generateByShrink(x, y, zoom, path, height=256, width=256):
# 	img1 = Image.open("%s/%d/%d/%d.png"%(path, zoom+1, x*2, y*2)).resize((int(width/2), int(height/2)), Image.ANTIALIAS)
# 	img2 = Image.open("%s/%d/%d/%d.png"%(path, zoom+1, x*2+1, y*2)).resize((int(width/2), int(height/2)), Image.ANTIALIAS)
# 	img3 = Image.open("%s/%d/%d/%d.png"%(path, zoom+1, x*2, y*2+1)).resize((int(width/2), int(height/2)), Image.ANTIALIAS)
# 	img4 = Image.open("%s/%d/%d/%d.png"%(path, zoom+1, x*2+1, y*2+1)).resize((int(width/2), int(height/2)), Image.ANTIALIAS)

# 	img = Image.new('RGB', (height, width))
# 	img.paste(img1, (0, 0))
# 	img.paste(img2, (int(width/2), 0))
# 	img.paste(img3, (0, int(height/2)))
# 	img.paste(img4, (int(width/2), int(height/2)))

# 	img1.close()
# 	img2.close()
# 	img3.close()
# 	img4.close()

# 	img.save("%s/%d/%d/%d.png"%(path, zoom, x, y))
# 	img.close()

# the input params shall be in the form (x, y, a, b, theta, color)
# where theta is degree and x,y,a,b is float and color in [0, 1]
def ellipse(data):
	x,y,a,b,theta,color = data
	R,G,B, _ = cm.hot(color)
	params = (x, y, a, b, theta, x, y, int(R*225), int(G*225), int(B*225))
	return '<ellipse cx="%f" cy="%f" rx="%f" ry="%f" transform="rotate(%f %f %f)" fill="#%02x%02x%02x"/>'%params

# to draw the image from data and scale it with x,y
def drawSvg(data, x, y, zoom, height=256, width=256):
	size = 1/(2**zoom)
	rangex = np.array([x*size, (x+1)*size])
	rangey = np.array([y*size, (y+1)*size])
	if data :
		data = np.array(data)
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


# using rsvg-convert for rendering
def generateByCreate(data, x, y, zoom, path, height=256, width=256):
	png = "%s/%d/%d/%d.png"%(path, zoom, x, y)
	jsn = "%s/%d/%d/%d.json"%(path, zoom, x, y)
	content = cairosvg.svg2png(drawSvg(data, x, y, zoom, height, width))

	pngfile = open(png, "wb")
	pngfile.write(content)
	pngfile.close()

	json_file = open(jsn, "w")
	json.dump(drawUTFMap(data, content, x, y, zoom, height, width), json_file)
	json_file.close()




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

def paste(grid, gridx, offsetx, offsety):
	for x in range(0, width, 2):
		for y in range(0, height, 2):
			grid[y/2+offsety][x/2+offsetx] = utfgrid_decode(gridx[y][x])

# def generateJSONByShrink(x, y, zoom, path, height=256, width=256):
# 	jsonFile1 = open("%s/%d/%d/%d.png"%(zoom+1, x*2, y*2), "r")
# 	json1 = json.load(jsonFile1)
# 	jsonFile2 = open("%s/%d/%d/%d.png"%(zoom+1, x*2+1, y*2), "r")
# 	json2 = json.load(jsonFile2)
# 	jsonFile3 = open("%s/%d/%d/%d.png"%(zoom+1, x*2, y*2+1), "r")
# 	json3 = json.load(jsonFile3)
# 	jsonFile4 = open("%s/%d/%d/%d.png"%(zoom+1, x*2+1, y*2), "r")
# 	json4 = json.load(jsonFile4)

# 	jsonFile1.close()
# 	jsonFile2.close()
# 	jsonFile3.close()
# 	jsonFile4.close()

# 	info = {}
# 	grid = numpy.zeros((width/2, height/2), type=np.uint8)

# 	paste(grid, json1['grid'], 0, 0)
# 	paste(grid, json2['grid'], width/2, 0)
# 	paste(grid, json3['grid'], 0, height/2)
# 	paste(grid, json4['grid'], width/2, height/2)

# 	keys = np.unique(grid)

# 	for k in keys:
# 		key = str(k)
# 		info[key] = json1["data"].get(key) or json2["data"].get(key) or json3["data"].get(key) or json4["data"].get(key)

# 	grid = ["".join(map(utfgrid_encode, line)) for line in grid]
# 	json_file = open("%s/%d/%d/%d.json"%(path, z, x, y), "w")
# 	json.dump({"grid": grid, "keys": list(key), "data": info}, json_file)

# will not consider interpolation at this moment.

def limit(x, domain):
	minx, maxx = domain
	return max(minx, min(maxx-1, x))

# it bares the question how we shall proceed
def drawUTFMap(data, raw_img, x, y, zoom, height=256, width=256):
	size = 1/(2**zoom)
	rangex = np.array([x*size, (x+1)*size])
	rangey = np.array([y*size, (y+1)*size])


	if data:
		data = np.array(data)
		data[:,0] = linear_scale(data[:, 0], rangex)*width/2 # x
		data[:,1] = linear_scale(data[:, 1], rangey)*height/2 # y
		data[:,2] = linear_scale(data[:, 2], [0, size])*width/2 # a
		data[:,3] = linear_scale(data[:, 3], [0, size])*height/2 # b

	# img = Image.open('%s/%d/%d/%d.png'%(path, zoom, x, y)).resize((int(width/2), int(height/2)), Image.NEAREST)
	img = Image.open(BytesIO(raw_img)).resize((int(width/2), int(height/2)), Image.NEAREST)

	# 3 is rely on the fact that it is rgb not rgba
	pixels = np.array(img.getdata()).reshape((width/2, height/2, 3))
	grid = np.zeros((width/2, height/2), dtype=np.uint8)
	info = {0 : {}}

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
			info[i+1] = {"x": x2, "y": y2, "a": a, "b": b, "theta": theta, "color": colour}

	grid = ["".join(map(utfgrid_encode, line)) for line in grid]
	
	return {"grid": grid, "keys": list(info.keys()), "data": info}
	

# we assume the x,y coord is in the range between 0 and 1
def splitData(data, zoom):
	size = 2**zoom
	data_group = [[[] for i in range(size+1)] for j in range(size+1)] # empty bins
	# put each datium to corresponding bin
	for datium in data:
		left = datium[0]-datium[2] # x-a
		right = datium[0]+datium[2] # x+a
		top = datium[1]-datium[2] # y-a
		bottom = datium[1]+datium[2] # y+a

		x1 = int(left*size)
		x2 = int(right*size)
		y1 = int(top*size)
		y2 = int(bottom*size)

		data_group[x1][y1].append(datium)
		data_group[x1][y2].append(datium) if y1!=y2 else None
		data_group[x2][y1].append(datium) if x1!=x2 else None
		data_group[x2][y2].append(datium) if (x1!=x2 and y1!=y2) else None
	return data_group

def createDir(path, zoom):
	for z in range(zoom+1):
		size = 2**z
		if (not os.path.isdir("%s/%d"%(path, z))): 
			try: os.mkdir("%s/%d"%(path, z))
			except: pass
		for i in range(size):
			if (not os.path.isdir("%s/%d/%d"%(path, z, i))):
				try: os.mkdir("%s/%d/%d"%(path, z, i))
				except: pass


def generate(path, data, zoom):
	for z in reversed(range(zoom+1)):
		data_group = splitData(data, z)
		size = 2**z
		for x in range(size):
			for y in range(size):
				tmp_write("generate file (%d, %d, %d)"%(z, x, y))
				generateByCreate(data_group[x][y], x, y, z, path)


def parseData(fileName):
	raw_data = pd.read_csv(fileName)
	valid_color = lambda x: -1<=x<=3
	valid_index, = np.where(raw_data.COLOR.map(valid_color))
	raw_data = raw_data.ix[valid_index]

	data = np.zeros((len(raw_data), 6))
	data[:,0] = minmax_scale(raw_data.DEC.values) # x
	data[:,1] = minmax_scale(raw_data.RA.values) # y
	data[:,2] = raw_data.A_IMAGE.values*0.263/3600*2 # a
	data[:,3] = raw_data.B_IMAGE.values*0.263/3600*2 # b
	data[:,4] = raw_data.THETA_IMAGE.values+90.
	data[:,5] = minmax_scale(raw_data.COLOR.values) # colour 

	return data

if __name__ == '__main__':
	path = os.path.abspath('./tiles')
	data = parseData("./test.csv")
	createDir(path, 7)
	generate(path, data, 7)



