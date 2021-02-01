import http.client
import json
import unittest

ADDRESS = "localhost:8000"

def request(method, path, data=None):
    headers = {}
    if data:
        headers = {"Content-Type": "application/json"}
        data = json.dumps(data)

    conn = http.client.HTTPConnection(ADDRESS)
    conn.request(method, path, data, headers)

    response = conn.getresponse()
    contents = response.read()
    contents = contents.decode('utf-8')
    if contents:
        try:
            contents = json.loads(contents)
        except json.decoder.JSONDecodeError as e:
            print("Failed to parse response as JSON:\n", contents)
            raise
    else:
        contents = None

    return contents, response.status

class RestComplianceTest(unittest.TestCase):

    def assertHateoas(self, todo):
        self.assertEqual(sorted(todo["links"], key=lambda x: x["rel"]), [
            {"rel": "delete", "url": "http://localhost:8000/todos/{}".format(todo["id"])},
            {"rel": "edit", "url": "http://localhost:8000/todos/{}".format(todo["id"])},
            {"rel": "self", "url": "http://localhost:8000/todos/{}".format(todo["id"])},
        ])

    def test_basic_restful_compliance(self):
        # Delete all todos
        out, code = request("DELETE", "/todos/")
        self.assertEqual(code, 204)
        self.assertEqual(out, None)

        # Retrieve all todos
        out, code = request("GET", "/todos/")
        self.assertEqual(code, 200)
        self.assertEqual(out, [])

        # Create three todos
        out, code = request("POST", "/todos/", {"name": "Do the ironing"})
        self.assertEqual(code, 201)
        self.assertEqual(out["name"], "Do the ironing")
        self.assertHateoas(out)

        out, code = request("POST", "/todos/", {"name": "Cook dinner"})
        self.assertEqual(code, 201)
        self.assertEqual(out["name"], "Cook dinner")
        self.assertHateoas(out)

        out, code = request("POST", "/todos/", {"name": "Exercise"})
        self.assertEqual(code, 201)
        self.assertEqual(out["name"], "Exercise")
        self.assertHateoas(out)

        # Edit todo
        out, code = request("PUT", "/todos/{}".format(out["id"]), {"name": "Watch TV"})
        self.assertEqual(code, 200)
        self.assertEqual(out["name"], "Watch TV")
        self.assertHateoas(out)

        # Get todo
        out, code = request("GET", "/todos/{}".format(out["id"]))
        self.assertEqual(code, 200)
        self.assertEqual(out["name"], "Watch TV")
        self.assertHateoas(out)

        out, code = request("GET", "/todos/")
        self.assertEqual(code, 200)

        for todo in out:
            self.assertHateoas(todo)

        to_delete = out[0]

        # Delete todo with id 1
        out, code = request("DELETE", "/todos/{}".format(to_delete["id"]))
        self.assertEqual(code, 204)
        self.assertEqual(out, None)

        # Get todo that does not exist
        out, code = request("GET", "/todos/qwertyu")
        self.assertEqual(code, 404)

        # Delete all todos
        out, code = request("DELETE", "/todos/")
        self.assertEqual(code, 204)
        self.assertEqual(out, None)

        # Retrieve all todos
        out, code = request("GET", "/todos/")
        self.assertEqual(code, 200)
        self.assertEqual(out, [])

if __name__ == "__main__":
    unittest.main()
