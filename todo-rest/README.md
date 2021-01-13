# Example Todo list application, using REST architectural pattern

This is an example Todo list application, which uses REST pattern for
for communication between client and a server.

The application is made of two components:

- Client written in Javascript + HTML + CSS (index.html, style.css, todo.js)
- Server written in Python using Flask web framework (main.py)

Application uses no database - todo list items are saved in memory.

# Server setup

1. Download and install Python 3

2. Install Flask.
```
python3 -m pip install flask
```

3. Run server
```
python3 server.py
```

# Client

Just open `index.html` with your browser.

# TODO

Currently the server implements REST Api level 1.

```
# Get all todos
GET /todos/

# Create todo
POST /todos/create

# Edit todo
POST /todos/edit/<id>

# Delete todo
POST /todos/delete/<id>

# Get one todo
GET /todos/<id>
```

## Task 1

The API needs to be RESTful (which means to implement level 3).

Example:
```
# Get all todos
GET /todos/

# Create todo
POST /todos/

# Edit todo
PUT /todos/<id>

# Delete todo
DELETE /todos/<id>

# Get one todo
GET /todos/<id>
```

To accomplish this you need to **change the API and the client** so that it implements level 3:

- Use http verbs (GET, POST, PUT, DELETE)
- Use proper response codes (201 - Created, 200 - Ok, 204 - No content, 202 - Accepted)
- Implement HATEOAS

**Fortunately**, the verification team provided a test case for the above scenarios,
which you can run using:

```
python3 test_todo.py
```

**Please, remember to make neccessary client adaptations (todo.js)**

## Task 2

Currently, user can input arbitrary HTML into the Todo list and the application does not escape it, before
it is displayed. This vulnerability is called XSS (Cross-site scripting).

Prevent basic XSS attack by escaping the contents of todo list items just before
they are displayed. 

You can use this function to do it:
```
function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }
```
