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

########################## EXIT #########################

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

def deleteData(_id, zoom=8):
	batch = leveldb.WriteBatch()
	for z in range(zoom):
		ezis = 2**(zoom-z)
		size = 2**z
		for x in range(size):
			for y in range(size):
				key = dataKey(_id, x, y, z)
				batch.Delete(key)
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

# read from CSV and parse data
# we use the database to store the data-key before it is will be intensely read
def saveData(_id, zoom=8):
	csv = open("./%s/data.csv"%_id, "r")
	data = mg.parseData(csv)
	csv.close()
	batch = leveldb.WriteBatch()
	for z in range(zoom+1):
		splited_data = mg.splitData(data, z)
		size = 2**z
		# ezis = 2**(zoom-z) # inverse size, stands for how large the datum chunk will be
		for x in range(size):
			for y in range(size):
				datum = np.array(splited_data[x][y])
				key = dataKey(_id, x, y, z)
				value = BytesIO()
				np.save(value, datum)
				batch.Put(key, value.getbuffer())
	db.Write(batch, sync=True)


def createMapDir(_id, zoom=8):
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

def generateTile(_id, z, x, y):
	key = dataKey(_id, x, y, z)
	value = BytesIO(db.Get(key))
	data = np.load(value)
	png, info = mg.generateByCreate(data, x, y, z)
	pngfile = open("./%s/%d/%d/%d.png"%(_id, z, x, y), "wb")
	pngfile.write(png)
	pngfile.close()
	infofile = open("./%s/%d/%d/%d.json"%(_id, z, x, y), "w")
	infofile.write(info)
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





