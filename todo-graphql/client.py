import http.client
import json

def request(query, vars={}):
    headers = {"Content-Type": "application/json"}

    conn = http.client.HTTPConnection("localhost:8000")
    conn.request("POST", "/graphql", json.dumps({"query": query, "variables": vars}) , headers)

    response = conn.getresponse()
    contents = response.read()
    contents = contents.decode('utf-8')
    contents = json.loads(contents)

    return contents

print(request("""
mutation{
    createTodo(name: "Cook dinner") {
        todo {
            id name
        }
    }
}
"""))

todos = request("""
query {
    todos {
        todos {
            id name
        }
    }
}
""")

print(todos)

print(request("""
mutation DeleteTodo($id: ID!) {
    deleteTodo(todoId: $id) {
        success
    }
}
""", {
    "id": todos["data"]["todos"]["todos"][0]["id"]
}))
