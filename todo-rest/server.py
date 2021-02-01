from flask import Flask, jsonify, request, abort
import uuid

app = Flask(__name__)

todos = [
	{"id": str(uuid.uuid4()), "name": "Clean up the room"},
	{"id": str(uuid.uuid4()), "name": "Cook dinner"},
	{"id": str(uuid.uuid4()), "name": "Iron clothes"},
]


def hateoas(todo):
	todo["links"] = [
		{"rel": "edit", "url": "http://127.0.0.1:8000/todos/{}".format(todo(["id"]))},
		{"rel": "self", "url": "http://127.0.0.1:8000/todos/{}".format(todo(["id"]))},
		{"rel": "delete", "url": "http://127.0.0.1:8000/todos/{}".format(todo(["id"]))}
	]


@app.route("/todos/", methods=["POST"])
def todo_new():
	todo = request.json
	todo["id"] = str(uuid.uuid4())
	todos.append(todo)
	return jsonify(hateoas(todo)), 201


@app.route("/todos/", methods=["GET"])
def todo_all():
	return jsonify(hateoas(todos)), 200


@app.route("/todos/<id>", methods=["DELETE"])
def todo_delete(id):
	todos[:] = [todo for todo in todos if todo["id"] != id]
	return "", 204


@app.route("/todos/", methods=["DELETE"])
def todo_all_delete():
	global last_id
	last_id = 0
	todos.clear()
	return "", 204


@app.route("/todos/<id>", methods=["PUT"])
def todo_edit(id):
	for todo in todos:
		if todo["id"] == id:
			todo["name"] = request.json["name"]
			return jsonify(hateoas(todo)), 200
	abort(404)


@app.route("/todos/<id>", methods=["GET"])
def todo_get(id):
	for todo in todos:
		if todo["id"] == id:
			return jsonify(hateoas(todo))
	abort(404)


@app.errorhandler(404)
def resource_not_found(e):
	return jsonify(), 404


@app.after_request
def cors(response):
	response.headers["Access-Control-Allow-Origin"] = "*"
	response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE,PUT"
	response.headers["Access-Control-Allow-Headers"] = "x-api-key,Content-Type"
	return response


if __name__ == "__main__":
	app.run(port=8000)
