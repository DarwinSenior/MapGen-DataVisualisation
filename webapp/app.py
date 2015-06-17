from flask import Flask, redirect, request, abort, send_file
import uuid, json
import database as db

app = Flask(__name__, static_url_path="")

@app.route('/')
def intropage():
	return redirect("/index.html")

@app.route('/maps', methods=["GET"])
def get_maps():
	return json.dumps(db.readMaps())

@app.route('/maps', methods=["PUT"])
def put_maps():
	name = request.form.get("name")
	new_entry = {
		"name" : name,
		"id" : str(uuid.uuid4()),
		"status" : 'uninitiated'
	}
	data = db.readMaps()
	data.append(new_entry)
	db.writeMaps(data)
	return json.dumps(data)

@app.route('/maps/load', methods=["POST"])
def init_maps():
		csv = request.files.get("csv")
		_id = request.form.get("id")
		if (_id and csv):
			data = db.readMaps()
			the_datum = None
			for datum in data:
				if datum['id'] == _id:
					the_datum = datum
			the_datum['status'] = 'loaded' 
			db.writeMaps(data)
			db.createMap(_id, csv)
			the_datum['status'] = 'ready'
			db.writeMaps(data)
			return json.dumps(data)
		else:
			abort(404)

@app.route('/maps', methods=["DELETE"])
def delete_maps():
	_id = request.form.get("id")
	data = db.readMaps()
	data = [item for item in data if item.get('id')!=_id]
	db.writeMaps(data)
	db.deleteMap(_id)
	return json.dumps(data)


@app.route('/map/<_id>', methods=["GET"])
def readInfo(_id):
	try:
		return json.dumps(db.readMeta(_id))
	except KeyError:
		abort(404)


@app.route('/map/<_id>', methods=["POST"])
def writeInfo(_id):
	metadata = db.readMeta(_id)
	try:
		if request.form.get('color') and request.form['color']!=metadata['color']:
			db.clearMap(_id)
			metadata['color'] = request.form['color']
		if request.form.get('infos'):
			metadata['infos'] = request.form['infos']
		db.writeMeta(_id, metadata)
		return json.dumps(metadata)
	except KeyError:
		abort(404)


@app.route('/tiles/<_id>/<int:z>/<int:x>/<int:y>', methods=["GET"])
def getTile(_id, z, x, y):
	if (_id in (item["id"] for item in db.readMaps())
		and 0<=x<2**z and 0<=y<2**z):
		return send_file("%s.png"%db.loadTile(_id, z, x, y))
	else:
		abort(404)

@app.route('/infos/<_id>/<int:z>/<int:x>/<int:y>', methods=["GET"])
def getInfo(_id, z, x, y):
	if (_id in (item["id"] for item in db.readMaps())
		and 0<=x<2**z and 0<=y<2**z):
		return send_file("%s.json"%db.loadTile(_id, z, x, y))
	else:
		abort(404)


if __name__ == "__main__":
	app.run(debug=True, use_reloader=False)