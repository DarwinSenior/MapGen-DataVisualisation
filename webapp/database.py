import json
import leveldb
import os
import shutil
import mapgen as mg
from io import BytesIO
import numpy as np

db = leveldb.LevelDB('./database', create_if_missing=True)
MAPS = b"maps"

try:
	db.Get(MAPS)
except:
	db.Put(MAPS, json.dumps([]).encode())

def readMaps():
	return json.loads(db.Get(MAPS).decode())

def writeMaps(data):
	data_json = json.dumps(data)
	db.Put(MAPS, data_json.encode())


########################## META #########################


'''
Specification of the meta-data
{
	"header" : <List>, // list of the names of the columns
	"color" : <string>, // contains the infomation on how to calculate the color
	"infos" : <List> // to find a way of displaying the infos
}
'''

def metaKey(_id):
	return ("meta-%s"%_id).encode()

def readMeta(_id):
	return json.loads(db.Get(metaKey(_id)).decode())

def writeMeta(_id, data):
	data_json = json.dumps(data)
	db.Put(metaKey(_id), data_json.encode())

# if the meta-data is changed, the data is invalidated, 
# remove all the png along with json but keep the csv
# and the meta-data
def clearMap(_id):
	'''
	only for linux and mac command, might need to change later
	'''
	os.system('find ./%s/ -name "*.png" -delete'%_id)
	os.system('find ./%s/ -name "*.json" -delete'%_id)

########################## EXIT #########################

# this will delete everything
def deleteMap(_id):
	try:
		deleteMapDir(_id)
		deleteData(_id)
		return True
		# return False
	except: 
		pass

def deleteMapDir(_id):
	shutil.rmtree("./%s"%_id)

def deleteData(_id, zoom=15):
	batch = leveldb.WriteBatch()
	for z in range(zoom+1):
		size = 2**z
		for x in range(size):
			for y in range(size):
				key = dataKey(_id, x, y, z)
				batch.Delete(key)
				key = infoKey(_id, x, y, z)
				batch.Delete(key)
	batch.Delete(metaKey(_id))
	db.Write(batch, sync=True)


######################## ENTER ########################

def createMap(_id, csv):
	createMapDir(_id)
	saveCSV(_id, csv)
	saveData(_id)
	return True

def saveCSV(_id, csv):
	csv.save("./%s/data.csv"%_id)

def dataKey(_id, x, y, z):
	return ("%s-%d.%d.%d"%(_id, x, y, z)).encode()

def infoKey(_id, x, y, z):
	return ("%s+%d.%d.%d"%(_id, x, y, z)).encode()

def saveData(_id, zoom=15):
	"""
	read from CSV and parse data
	we use the database to store the data-key before it is will be intensely read
	"""
	csv = open("./%s/data.csv"%_id, "r")
	# data = mg.parseData(csv)
	data, info, header = mg.parseData(csv)
	csv.close()
	batch = leveldb.WriteBatch()
	for z in range(zoom+1):
		# splited_data = mg.splitData(data, z)
		splitted_data, splitted_info = mg.splitData(data, info, z)
		size = 2**z

		for x in range(size):
			for y in range(size):
				datum = np.array(splitted_data[x][y])
				# key = dataKey(_id, x, y, z)
				datakey = dataKey(_id, x, y, z)
				value = BytesIO()
				np.save(value, datum)
				# batch.Put(key, value.getbuffer())
				batch.Put(datakey, value.getbuffer())
				infokey= infoKey(_id, x, y, z)
				batch.Put(infokey, json.dumps(splitted_info[x][y]).encode())
		meta = {'header': header, 'color': '', 'infos': ''}
		writeMeta(_id, meta)
	db.Write(batch, sync=True)


def createMapDir(_id, zoom=15):
	os.mkdir("./%s"%_id)
	for z in range(zoom+1):
		size = 2**z
		if (not os.path.isdir("./%s/%d"%(_id, z))): 
			try: os.mkdir("./%s/%d"%(_id, z))
			except: pass
		for i in range(size):
			if (not os.path.isdir("./%s/%d/%d"%(_id, z, i))):
				try: os.mkdir("./%s/%d/%d"%(_id, z, i))
				except: pass

def csvColumns(_id, splitter=","):
	"""
	Read the first line and get the header,
	so, the header shall be in the following form
	'RA,DEC,A_IMAGE,B_IMAGE,THETA_IMAGE,COLOR,TILENAME\n'
	"""
	csvfile = open("./%s/data.csv"%_id, "r")
	columns = csvfile.readline().strip().split(splitter)
	csvfile.close()
	return columns

def generateTile(_id, z, x, y):
	value = BytesIO(db.Get(dataKey(_id, x, y, z)))
	data = np.load(value)
	# meta = json.loads(db.Get(metaKey(_id)).decode())
	info = json.loads(db.Get(infoKey(_id, x, y, z)).decode())
	color = readMeta(_id)['color']
	png, jsn = mg.generateByCreate(data, info, x, y, z, color)

	pngfile = open("./%s/%d/%d/%d.png"%(_id, z, x, y), "wb")
	pngfile.write(png)
	pngfile.close()
	infofile = open("./%s/%d/%d/%d.json"%(_id, z, x, y), "w")
	infofile.write(jsn)
	infofile.close()

########################### UPDATE ################################

# it is an lazy init to make sure that the tile is generated properly
def loadTile(_id, z, x, y):
	if not (os.path.isfile("./%s/%d/%d/%d.png"%(_id, z, x, y)) 
			and os.path.isfile("./%s/%d/%d/%d.json"%(_id, z, x, y))):
		generateTile(_id, z, x, y)
	return "./%s/%d/%d/%d"%(_id, z, x, y)


########################### UTIL #################################

def clearAll():
	for item in readMaps():
		_id = item["id"]
		print("delete id: <%s>"%_id)
		deleteMap(_id)
		db.Put(MAPS, json.dumps([]).encode())





