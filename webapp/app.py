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
	csv = request.files.get("csv")
	new_entry = {
		"name" : name,
		"id" : str(uuid.uuid4())
	}
	print(name, csv)
	if (name and csv):
		data = db.readMaps()
		data.append(new_entry)
		db.writeMaps(data)
		db.createMap(new_entry["id"], csv)
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

@app.route('/tiles/<_id>/<int:z>/<int:x>/<int:y>', methods=["GET"])
def getTile(_id, z, x, y):
	if (_id in (item["id"] for item in db.readMaps())
		and 0<=x<2**z and 0<=y<2**z):
		print(x, y, 2**z)
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