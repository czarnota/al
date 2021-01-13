from flask import Flask, jsonify, request, abort
import uuid

app = Flask(__name__)

todos = [
    { "id": str(uuid.uuid4()), "name": "Clean up the room" },
    { "id": str(uuid.uuid4()), "name": "Cook dinner" },
    { "id": str(uuid.uuid4()), "name": "Iron clothes" },
]

@app.route("/todos/create", methods=["POST"])
def todo_new():
    todo = request.json
    todo["id"] = str(uuid.uuid4())
    todos.append(todo)
    return jsonify(todo)

@app.route("/todos/", methods=["GET"])
def todo_all():
    return jsonify(todos)

@app.route("/todos/delete/<id>", methods=["POST"])
def todo_delete(id):
    todos[:] = [ todo for todo in todos if todo["id"] != id ]
    return jsonify({})

@app.route("/todos/delete_all", methods=["POST"])
def todo_all_delete():
    global last_id
    last_id = 0
    todos.clear()
    return jsonify([])

@app.route("/todos/edit/<id>", methods=["POST"])
def todo_edit(id):
    for todo in todos:
        if todo["id"] == id:
            todo["name"] = request.json["name"]
            return jsonify(todo)
    abort(404)

@app.route("/todos/<id>", methods=["GET"])
def todo_get(id):
    for todo in todos:
        if todo["id"] == id:
            return jsonify(todo)
    abort(404)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(), 404

@app.after_request
def cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST"
    response.headers["Access-Control-Allow-Headers"] = "x-api-key,Content-Type"
    return response

if __name__ == "__main__":
    app.run(port=8000)
