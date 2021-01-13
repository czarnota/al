from suds.client import Client

c = Client("http://localhost:8000/?wsdl")

todo = c.factory.create("Todo")
todo.name = "Do the ironing"
c.service.createTodo(todo)

todo = c.factory.create("Todo")
todo.name = "Prepare dinner"
c.service.createTodo(todo)

todo = c.factory.create("Todo")
todo.name = "Go shopping"
c.service.createTodo(todo)

print(c.service.getTodos())

# (TodoArray){
#       (Todo){
#         name = "Do the ironing"
#      },
#      (Todo){
#         name = "Prepare dinner"
#      },
#      (Todo){
#         name = "Go shopping"
#      },
# }
