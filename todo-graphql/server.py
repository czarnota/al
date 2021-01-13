from flask import Flask, request, jsonify
import ariadne, uuid

app = Flask(__name__)

todos = [
    { "id": str(uuid.uuid4()), "name": "Cook dinner" },
    { "id": str(uuid.uuid4()), "name": "Do the ironing" },
    { "id": str(uuid.uuid4()), "name": "Shave" },
]

def resolve_todos(obj, info):
    return { "todos": todos, "success": True }

@ariadne.convert_kwargs_to_snake_case
def resolve_todo(obj, info, todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            return { "success": True, "todo": todo }
    return { "success": False, "errors": [ "Unable to find todo" ] }

@ariadne.convert_kwargs_to_snake_case
def resolve_create_todo(obj, info, name):
    todo = {"id": str(uuid.uuid4()), "name": name}
    todos.append(todo)
    return {"success": True, "todo": todo}

@ariadne.convert_kwargs_to_snake_case
def resolve_delete_todo(obj, info, todo_id):
    for i, todo in enumerate(todos):
        print(todo_id, todo["id"])
        if todo["id"] == todo_id:
            del todos[i]
            return { "success": True }
    return { "success": False, "errors": [ "Can't find todo" ] }

query = ariadne.ObjectType("Query")
query.set_field("todos", resolve_todos)
query.set_field("todo", resolve_todo)

mutation = ariadne.ObjectType("Mutation")
mutation.set_field("createTodo", resolve_create_todo)
mutation.set_field("deleteTodo", resolve_delete_todo)

schema = ariadne.make_executable_schema(ariadne.load_schema_from_path("schema.graphql"),
                                        query,
                                        mutation,
                                        ariadne.snake_case_fallback_resolvers)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    data = request.args.get("query")
    if data:
        success, result = ariadne.graphql_sync(
            schema,
            {"query": data},
            context_value=request,
            debug=app.debug
        )

        status_code = 200 if success else 400
        return jsonify(result), status_code
    return ariadne.constants.PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = ariadne.graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

app.run(port=8000)
