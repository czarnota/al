import CORBA, TodoList, TodoList__POA, CosNaming, sys, uuid

class TodoService(TodoList__POA.TodoService):
    def __init__(self):
        self.todos = []

    def createTodo(self, t):
        t.id = str(uuid.uuid1())
        self.todos.append(t)
        return t.id

    def deleteTodo(self, id):
        for i, todo in enumerate(self.todos):
            if todo.id == id:
                del self.todos[i];

    def getTodo(self, id):
        for todo in self.todos:
            if todo.id == id:
                return todo;
        return TodoList.Todo(id="", name="")

    def getTodos(self):
        return self.todos

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

ts = TodoService()
ts_ref = ts._this()

orb.resolve_initial_references("RootPOA")._get_the_POAManager().activate()

# Find name service
ns = orb.resolve_initial_references("NameService")._narrow(CosNaming.NamingContext)
# Bind a context named "todo.ctx" to the root context
name = [CosNaming.NameComponent("todo", "ctx")]
ctx = None
try:
    ctx = ns.bind_new_context(name)
except CosNaming.NamingContext.AlreadyBound as ex:
    ctx = ns.resolve(name)._narrow(CosNaming.NamingContext)
# The full name will be todo.ctx/TodoService.Object
name = [CosNaming.NameComponent("TodoService", "Object")]
try:
    ctx.bind(name, ts_ref)
except CosNaming.NamingContext.AlreadyBound:
    ctx.rebind(name, ts_ref)

orb.run()

