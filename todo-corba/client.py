#!/usr/bin/env python

import CORBA
import TodoList, TodoList__POA, CosNaming
import sys

# Initialize Object Request Broker
orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

ns = orb.resolve_initial_references("NameService")._narrow(CosNaming.NamingContext)

obj = ns.resolve([CosNaming.NameComponent("todo", "ctx"), CosNaming.NameComponent("TodoService", "Object")])

todo_service = obj._narrow(TodoList.TodoService)


todo = TodoList.Todo(id="", name="Do the laundry")
todo_service.createTodo(todo)

todo = TodoList.Todo(id="", name="Exercise")
todo_service.createTodo(todo)

todo = TodoList.Todo(id="", name="Prepare dinner")
todo_service.createTodo(todo)

todo = TodoList.Todo(id="", name="Do the ironing")
uuid = todo_service.createTodo(todo)

todo = todo_service.getTodo(uuid)
print(todo)

todo_service.deleteTodo(uuid)

todo = todo_service.getTodo(uuid)
print(todo)

todos = todo_service.getTodos()
print(todos)
